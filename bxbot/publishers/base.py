"""Publisher 协议与智能分流调度。"""

from __future__ import annotations

from typing import Protocol

from loguru import logger

from bxbot.models import MediaKind, PublishBundle, PublishResult


class Publisher(Protocol):
    async def publish_video(self, bundle: PublishBundle) -> PublishResult: ...
    async def publish_image_dynamic(self, bundle: PublishBundle) -> PublishResult: ...
    async def publish_text_dynamic(self, bundle: PublishBundle) -> PublishResult: ...


class PublishDispatcher:
    """按媒体类型分流：视频→视频稿件；图片→图文动态；纯文字→文字动态。"""

    def __init__(self, publisher: Publisher):
        self._publisher = publisher

    async def publish(self, bundle: PublishBundle) -> PublishResult:
        kind = bundle.tweet.media_kind
        if kind in (MediaKind.VIDEO, MediaKind.GIF, MediaKind.MIXED):
            if not bundle.media_files:
                logger.warning(f"{bundle.tweet.tweet_id} 视频缺失，降级为文字动态")
                return await self._publisher.publish_text_dynamic(bundle)
            return await self._publisher.publish_video(bundle)
        if kind == MediaKind.PHOTO and bundle.media_files:
            return await self._publisher.publish_image_dynamic(bundle)
        return await self._publisher.publish_text_dynamic(bundle)
