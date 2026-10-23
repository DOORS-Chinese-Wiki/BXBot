"""B 站视频稿件投稿：UPOS 分片上传 + 提交稿件。"""

from __future__ import annotations

from pathlib import Path

from loguru import logger

from bxbot.publishers.bilibili.risk import wrap_bili_errors


class VideoPublisher:
    def __init__(self, cred):
        self._cred = cred

    @wrap_bili_errors
    async def publish(
        self,
        *,
        video_path: Path,
        cover_path: Path,
        title: str,
        desc: str,
        tags: list[str],
        tid: int,
        source_url: str,
        dynamic_text: str = "",
    ) -> dict:
        from bilibili_api import Picture, video_uploader

        meta = video_uploader.VideoMeta(
            tid=tid,
            title=title[:80],
            desc=desc[:2000],
            cover=Picture.from_file(str(cover_path)),
            tags=tags,
            original=False,  # 搬运 → copyright=2（转载）
            source=source_url,  # 转载来源 = 原推链接
            dynamic=dynamic_text[:233] if dynamic_text else "",
        )
        page = video_uploader.VideoUploaderPage(
            path=str(video_path),
            title=title[:80],
            description="",
        )
        uploader = video_uploader.VideoUploader([page], meta, self._cred)

        uploader.add_event_listener(
            video_uploader.VideoUploaderEvents.SUBMIT_FAILED.value,
            lambda data: logger.error(f"稿件提交失败：{data}"),
        )
        uploader.add_event_listener(
            video_uploader.VideoUploaderEvents.FAILED.value,
            lambda data: logger.error(f"上传失败：{data}"),
        )

        result = await uploader.start()
        logger.info(f"视频稿件已提交：{result}")
        return result or {}
