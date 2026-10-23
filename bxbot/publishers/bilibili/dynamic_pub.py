"""B 站动态发布：文字/图文动态（按 owner-bili-apis 新版接口流程）。

- 纯文本：submit_check → create/dyn
- 图文：upload_bfs（每图）→ submit_check → create/dyn
"""

from __future__ import annotations

from pathlib import Path

from loguru import logger

from bxbot.publishers.bilibili.dyn_api import (
    BiliDynClient,
    build_content,
    build_create_dyn_body,
    build_pics,
    build_submit_check_body,
    make_upload_id,
)


class DynamicPublisher:
    def __init__(self, client: BiliDynClient, *, aigc_flag: int = 0):
        self._client = client
        self._aigc = aigc_flag

    async def publish_text(self, text: str, title: str = "") -> dict:
        content = build_content(text, title)
        check_body = build_submit_check_body(content, aigc_flag=self._aigc)
        await self._client.submit_check(check_body)

        body = build_create_dyn_body(
            content,
            upload_id=make_upload_id(self._client.mid),
            aigc_flag=self._aigc,
        )
        data = await self._client.create_dyn(body)
        return {
            "dyn_id_str": str(data.get("dyn_id_str") or ""),
            "dyn_rid": str(data.get("dyn_rid") or ""),
        }

    async def publish_images(
        self, text: str, image_paths: list[Path], title: str = ""
    ) -> dict:
        # 1) 逐图上传 BFS 图床
        pics: list[dict] = []
        for p in image_paths:
            pics.append(await self._client.upload_bfs(p))
        pics = build_pics(pics)

        # 2) 提交前检查
        content = build_content(text, title)
        check_body = build_submit_check_body(content, pics=pics, aigc_flag=self._aigc)
        await self._client.submit_check(check_body)

        # 3) 正式发布
        body = build_create_dyn_body(
            content,
            upload_id=make_upload_id(self._client.mid),
            pics=pics,
            aigc_flag=self._aigc,
        )
        data = await self._client.create_dyn(body)
        logger.info(
            f"图文动态已发送（{len(pics)} 图）：dyn_id={data.get('dyn_id_str')}"
        )
        return {
            "dyn_id_str": str(data.get("dyn_id_str") or ""),
            "dyn_rid": str(data.get("dyn_rid") or ""),
        }
