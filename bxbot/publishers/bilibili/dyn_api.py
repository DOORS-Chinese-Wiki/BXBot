"""新版动态发布 HTTP 层（按 owner-bili-apis 文档实现）。

流程：
- 纯文本：submit_check → create/dyn（两步）
- 图文：upload_bfs（每图）→ submit_check（带 pics）→ create/dyn（三步）

接口：
- POST /x/dynamic/feed/draw/upload_bfs        （multipart，csrf）
- POST /x/dynamic/feed/create/submit_check    （JSON，csrf）
- POST /x/dynamic/feed/create/dyn             （JSON，csrf + WBI + 风控参数）
"""

from __future__ import annotations

import random
import time
from pathlib import Path

import httpx
from loguru import logger

from bxbot.pipeline import BiliContentRejected, BiliRiskError
from bxbot.publishers.bilibili.risk import is_risk_error
from bxbot.publishers.bilibili.wbi import WbiSigner

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_REFERER = "https://t.bilibili.com/"


# ---- 纯函数：请求体构造（便于单测）----


def build_content(text: str, title: str = "") -> dict:
    return {
        "contents": [{"raw_text": text, "type": 1, "biz_id": ""}],
        "title": title,
    }


def build_pics(items: list[dict]) -> list[dict]:
    """items: [{img_src, img_width, img_height, img_size, ai_gen_pic?}]"""
    pics = []
    for it in items:
        pics.append(
            {
                "img_src": it["img_src"],
                "img_width": it.get("img_width", 0),
                "img_height": it.get("img_height", 0),
                "img_size": it.get("img_size", 0),
                "ai_gen_pic": it.get("ai_gen_pic", 0),
            }
        )
    return pics


def make_upload_id(
    mid: str | int, ts: int | None = None, rnd: int | None = None
) -> str:
    """upload_id 格式：{mid}_{timestamp}_{随机数}（文档约定）。"""
    return f"{mid}_{int(ts if ts is not None else time.time())}_{rnd if rnd is not None else random.randint(1000, 9999)}"


def build_submit_check_body(
    content: dict, pics: list[dict] | None = None, aigc_flag: int = 0
) -> dict:
    body: dict = {
        "content": content,
        "scene": 2,
        "attach_card": None,
    }
    if pics:
        body["create_option"] = {"aigc": aigc_flag, "pic_mode": 0}
        body["pics"] = pics
    else:
        body["option"] = {
            "aigc": aigc_flag,
            "private_pub": 0,
            "up_choose_comment": 0,
        }
    return body


def build_create_dyn_body(
    content: dict, upload_id: str, pics: list[dict] | None = None, aigc_flag: int = 0
) -> dict:
    dyn_req: dict = {
        "content": content,
        "scene": 2,
        "attach_card": None,
        "upload_id": upload_id,
        "meta": {"app_meta": {"from": "create.dynamic.web", "mobi_app": "web"}},
    }
    if pics:
        dyn_req["option"] = {"aigc": aigc_flag, "pic_mode": 0}
        dyn_req["pics"] = pics
    else:
        dyn_req["option"] = {
            "aigc": aigc_flag,
            "private_pub": 0,
            "up_choose_comment": 0,
        }
    return {"dyn_req": dyn_req}


# ---- HTTP 客户端 ----


class BiliApiError(Exception):
    """B 站接口返回非 0 code。"""

    def __init__(self, code: int, message: str):
        super().__init__(f"bili api code={code}: {message}")
        self.code = code
        self.message = message


class BiliDynClient:
    def __init__(
        self,
        cookies: dict[str, str],
        mid: str | int,
        *,
        proxy: str = "",
        risk_params: dict[str, str] | None = None,
        timeout_s: float = 30.0,
    ):
        self._mid = str(mid)
        self._risk_params = dict(risk_params or {})
        self._cookies = {k: v for k, v in cookies.items() if v}
        cookie_header = "; ".join(f"{k}={v}" for k, v in self._cookies.items())
        self._client = httpx.AsyncClient(
            proxy=proxy or None,
            timeout=httpx.Timeout(timeout_s),
            headers={
                "User-Agent": _UA,
                "Referer": _REFERER,
                "Origin": "https://t.bilibili.com",
                "Cookie": cookie_header,
            },
        )
        self._wbi = WbiSigner(self._client)

    @property
    def mid(self) -> str:
        return self._mid

    async def close(self) -> None:
        await self._client.aclose()

    # ---- 图片上传 ----

    async def upload_bfs(self, image_path: Path) -> dict:
        """POST /x/dynamic/feed/draw/upload_bfs → {img_src, img_width, img_height, img_size}"""
        data = {"biz": "new_dyn", "category": "daily", "csrf": self._csrf}
        with open(image_path, "rb") as f:
            files = {"file_up": (image_path.name, f, _guess_mime(image_path))}
            resp = await self._client.post(
                "https://api.bilibili.com/x/dynamic/feed/draw/upload_bfs",
                data=data,
                files=files,
            )
        payload = self._check(resp, context="upload_bfs")
        d = payload.get("data") or {}
        if not d.get("image_url"):
            raise BiliApiError(-1, f"upload_bfs 未返回 image_url：{payload}")
        logger.info(f"BFS 图片已上传：{image_path.name} → {d['image_url'][:60]}…")
        return {
            "img_src": d["image_url"],
            "img_width": d.get("image_width", 0),
            "img_height": d.get("image_height", 0),
            "img_size": d.get("img_size", 0),
            "ai_gen_pic": d.get("ai_gen_pic", 0),
        }

    # ---- 提交前检查 ----

    async def submit_check(self, body: dict) -> None:
        """POST /x/dynamic/feed/create/submit_check。不通过 → BiliContentRejected。"""
        resp = await self._client.post(
            "https://api.bilibili.com/x/dynamic/feed/create/submit_check",
            params={"csrf": self._csrf},
            json=body,
        )
        payload = self._check(resp, context="submit_check")
        data = payload.get("data") or {}
        if data.get("pass") is False:
            raise BiliContentRejected(f"submit_check 未通过：{payload}")
        logger.debug("submit_check 通过")

    # ---- 正式发布 ----

    async def create_dyn(self, body: dict) -> dict:
        """POST /x/dynamic/feed/create/dyn（WBI + 风控参数）→ 响应 data。"""
        params = self._build_query_params()
        signed = await self._wbi.sign(params)
        resp = await self._client.post(
            "https://api.bilibili.com/x/dynamic/feed/create/dyn",
            params=signed,
            json=body,
        )
        try:
            payload = self._check(resp, context="create_dyn")
        except BiliApiError as e:
            # WBI 签名失效（key 每日更替）：刷新后重试一次
            if e.code == -400 or "v_voucher" in str(resp.text):
                logger.info("WBI 签名可能过期，刷新 key 后重试一次")
                self._wbi.invalidate()
                signed = await self._wbi.sign(self._build_query_params())
                resp = await self._client.post(
                    "https://api.bilibili.com/x/dynamic/feed/create/dyn",
                    params=signed,
                    json=body,
                )
                payload = self._check(resp, context="create_dyn(retry)")
            else:
                raise
        data = payload.get("data") or {}
        logger.info(f"动态已发布：dyn_id={data.get('dyn_id_str')}")
        return data

    async def remove_dynamic(
        self, dyn_id_str: str, dyn_type: int = 2, rid_str: str = ""
    ) -> None:
        """POST /x/dynamic/feed/operate/remove（仅需 CSRF）。"""
        resp = await self._client.post(
            "https://api.bilibili.com/x/dynamic/feed/operate/remove",
            params={"platform": "web", "csrf": self._csrf},
            json={
                "dyn_id_str": str(dyn_id_str),
                "dyn_type": dyn_type,
                "rid_str": str(rid_str),
            },
        )
        self._check(resp, context="remove_dynamic")
        logger.info(f"动态已删除：{dyn_id_str}")

    # ---- 内部 ----

    @property
    def _csrf(self) -> str:
        return self._cookies.get("bili_jct", "")

    def _build_query_params(self) -> dict:
        params: dict = {
            "platform": "web",
            "csrf": self._csrf,
            "w_dyn_req.upload_id": make_upload_id(self._mid),
            "w_dyn_req.meta": '{"app_meta":{"from":"create.dynamic.web"}}',
        }
        # 风控参数透传（b_wet / dm_*，浏览器抓包值；缺失可能导致 -403）
        params.update(self._risk_params)
        return params

    @staticmethod
    def _check(resp: httpx.Response, *, context: str) -> dict:
        try:
            payload = resp.json()
        except Exception as e:
            raise BiliApiError(
                resp.status_code, f"{context} 非 JSON 响应：{resp.text[:120]}"
            ) from e
        code = payload.get("code", resp.status_code)
        message = str(payload.get("message", ""))
        if code == 0:
            return payload
        err = BiliApiError(int(code), f"{context}: {message}")
        if is_risk_error(err):
            raise BiliRiskError(str(err)) from err
        raise err


def _guess_mime(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")
