"""统一领域模型：推文、媒体、LLM 结果、发布结果。"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class TweetStatus(str, Enum):
    PENDING = "pending"  # 已发现，待处理
    FILTERED = "filtered"  # 规则/LLM 判定跳过（终态）
    PUBLISHED = "published"  # 已发布成功（终态）
    FAILED = "failed"  # 重试耗尽（终态）；attempt < max 时可重试


class MediaKind(str, Enum):
    NONE = "none"
    PHOTO = "photo"
    VIDEO = "video"
    GIF = "gif"
    MIXED = "mixed"


class MediaAsset(BaseModel):
    """推文里的一个媒体文件（尚未下载）。"""

    kind: MediaKind
    url: str  # 图片原图 / mp4 直链
    thumbnail_url: str | None = None
    width: int | None = None
    height: int | None = None
    duration_s: float | None = None
    bitrate: int | None = None  # 用于 mp4 清晰度选择


class NormalizedTweet(BaseModel):
    """各抓取后端统一后的推文模型。"""

    tweet_id: str
    author_handle: str
    author_id: str = ""
    text: str  # 原文
    lang: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    url: str
    is_retweet: bool = False
    is_reply: bool = False
    is_quote: bool = False
    media: list[MediaAsset] = Field(default_factory=list)
    url_entities: dict[str, str] = Field(default_factory=dict)  # t.co → 真实链接
    source_fetcher: str = ""

    @property
    def media_kind(self) -> MediaKind:
        if not self.media:
            return MediaKind.NONE
        kinds = {m.kind for m in self.media}
        has_video = bool(kinds & {MediaKind.VIDEO, MediaKind.GIF})
        has_photo = MediaKind.PHOTO in kinds
        if has_video and has_photo:
            return MediaKind.MIXED
        if has_video:
            return MediaKind.VIDEO if MediaKind.VIDEO in kinds else MediaKind.GIF
        return MediaKind.PHOTO


class LLMResult(BaseModel):
    """LLM 单次调用产出：译文 + 同步判断 + 发布辅助信息。"""

    translate_zh: str
    should_sync: bool
    reason: str = ""
    title_zh: str | None = None
    tags: list[str] = Field(default_factory=list)


class PublishResult(BaseModel):
    ok: bool
    kind: str  # "video" | "image_dynamic" | "text_dynamic" | "dry_run"
    bvid: str | None = None
    dynamic_id: str | None = None
    dyn_rid: str | None = None  # 删除动态时需要
    error: str | None = None
    dry_run_preview: str | None = None


class PublishBundle(BaseModel):
    """发布阶段的完整输入。"""

    tweet: NormalizedTweet
    llm: LLMResult
    text_final: str  # 动态正文（含 #话题# 后缀）
    desc_final: str | None = None  # 视频稿件简介（不含话题，标签走 tag 字段）
    title: str
    tags: list[str]
    tid: int
    media_files: list[Path] = Field(default_factory=list)
    cover_path: Path | None = None
