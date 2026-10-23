"""BiliPublisher：实现 Publisher 协议，组合动态（新版直连接口）/视频（库）发布器。"""

from __future__ import annotations

from loguru import logger

from bxbot.config import Config
from bxbot.models import PublishBundle, PublishResult
from bxbot.publishers.bilibili import auth
from bxbot.publishers.bilibili.audit import get_audit_status
from bxbot.publishers.bilibili.dyn_api import BiliDynClient
from bxbot.publishers.bilibili.dynamic_pub import DynamicPublisher
from bxbot.publishers.bilibili.video_pub import VideoPublisher


class BiliCredentialsMissing(Exception):
    pass


class BiliPublisher:
    def __init__(self, cred, cfg: Config, *, mid: str = "", uname: str = ""):
        self._cred = cred
        self._cfg = cfg
        self._mid = mid
        self._uname = uname
        self._cookies = auth.cred_to_cookies(cred)
        self._dyn_client = BiliDynClient(
            self._cookies,
            mid=mid or "0",
            proxy=cfg.bilibili.proxy,
            risk_params=cfg.bilibili.risk_params,
        )
        self._dynamic = DynamicPublisher(
            self._dyn_client, aigc_flag=cfg.bilibili.aigc_flag
        )
        self._video = VideoPublisher(cred)

    @classmethod
    async def create(cls, cfg: Config) -> BiliPublisher:
        from bilibili_api import request_settings

        if cfg.bilibili.proxy:
            request_settings.set_proxy(cfg.bilibili.proxy)

        cred = auth.load_cred(cfg.bili_cred_path)
        if cred is None or not cred.sessdata or not cred.bili_jct:
            raise BiliCredentialsMissing(
                "B 站凭证缺失或不完整，请先运行：python -m bxbot login-bili"
            )
        try:
            info = await auth.probe(cred)
            logger.info(
                f"B 站登录有效：{info.get('uname', '?')} (uid={info.get('mid', '?')})"
            )
        except Exception as e:
            raise BiliCredentialsMissing(
                f"B 站凭证已失效（{e}），请重新运行：python -m bxbot login-bili"
            ) from e
        return cls(
            cred, cfg, mid=str(info.get("mid", "")), uname=str(info.get("uname", ""))
        )

    async def close(self) -> None:
        await self._dyn_client.close()

    # ---- Publisher 协议 ----

    async def publish_video(self, bundle: PublishBundle) -> PublishResult:
        assert bundle.cover_path is not None
        result = await self._video.publish(
            video_path=bundle.media_files[0],
            cover_path=bundle.cover_path,
            title=bundle.title,
            desc=bundle.desc_final
            if bundle.desc_final is not None
            else bundle.text_final,
            tags=bundle.tags,
            tid=bundle.tid,
            source_url=bundle.tweet.url,
            dynamic_text="",
        )
        bvid = str(result.get("bvid") or "") or None
        # 投稿后查一次审核状态（异步审核，仅记录）
        if bvid:
            try:
                await get_audit_status(
                    bvid, self._cookies, proxy=self._cfg.bilibili.proxy
                )
            except Exception as e:
                logger.warning(f"审核状态查询失败（不影响发布）：{e}")
        return PublishResult(ok=True, kind="video", bvid=bvid)

    async def publish_image_dynamic(self, bundle: PublishBundle) -> PublishResult:
        result = await self._dynamic.publish_images(
            bundle.text_final, bundle.media_files, title=""
        )
        return PublishResult(
            ok=True,
            kind="image_dynamic",
            dynamic_id=_extract_dynamic_id(result),
            dyn_rid=result.get("dyn_rid") or None,
        )

    async def publish_text_dynamic(self, bundle: PublishBundle) -> PublishResult:
        result = await self._dynamic.publish_text(bundle.text_final, title="")
        return PublishResult(
            ok=True,
            kind="text_dynamic",
            dynamic_id=_extract_dynamic_id(result),
            dyn_rid=result.get("dyn_rid") or None,
        )

    async def delete_dynamic(
        self, dyn_id: str, dyn_rid: str = "", dyn_type: int = 2
    ) -> None:
        """删除已发布动态（运维用）。"""
        await self._dyn_client.remove_dynamic(
            dyn_id, dyn_type=dyn_type, rid_str=dyn_rid
        )


def _extract_dynamic_id(result: dict) -> str | None:
    if not result:
        return None
    for key in ("dyn_id_str", "dyn_id", "id_str", "id", "dynamic_id"):
        if result.get(key):
            return str(result[key])
    data = result.get("data") if isinstance(result.get("data"), dict) else {}
    for key in ("dyn_id_str", "dyn_id", "id_str", "id"):
        if data.get(key):
            return str(data[key])
    return None
