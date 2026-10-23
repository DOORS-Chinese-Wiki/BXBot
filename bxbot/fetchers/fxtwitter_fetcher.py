"""FxTwitter 公共 API 后端：免鉴权查单条推文（不能拉时间线）。"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from bxbot.fetchers.base import FetchError
from bxbot.models import MediaAsset, MediaKind, NormalizedTweet

_API = "https://api.fxtwitter.com/2/status/{tweet_id}"


class FxTwitterFetcher:
    name = "fxtwitter"
    supports_timeline = False  # 公共 API 只有单条查询

    def __init__(self, proxy: str = "", timeout_s: float = 20.0):
        self._proxy = proxy or None
        self._timeout = timeout_s
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        self._client = httpx.AsyncClient(
            proxy=self._proxy,
            timeout=httpx.Timeout(self._timeout),
            headers={"User-Agent": "BXBot/0.1 (sync bot)"},
            follow_redirects=True,
        )

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def fetch_user_timeline(
        self, *, target_handle: str, since_id: str | None, limit: int = 20
    ) -> list[NormalizedTweet]:
        raise FetchError("fxtwitter 不支持时间线拉取（仅单条查询）")

    async def fetch_tweet(self, tweet_id: str) -> NormalizedTweet | None:
        assert self._client is not None
        try:
            resp = await self._client.get(_API.format(tweet_id=tweet_id))
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise FetchError(
                f"fxtwitter 查询失败 {tweet_id}: {type(e).__name__}: {e}"
            ) from e
        if data.get("code") != 200:
            raise FetchError(
                f"fxtwitter 返回 code={data.get('code')} msg={data.get('message')}"
            )
        status = data.get("status") or {}
        return self._normalize(status)

    def _normalize(self, s: dict[str, Any]) -> NormalizedTweet:
        author = s.get("author") or {}
        handle = author.get("screen_name") or ""
        tweet_id = str(s.get("id"))
        created = s.get("created_at")
        try:
            created_at = (
                datetime.fromisoformat(created.replace("Z", "+00:00"))
                if created
                else datetime.now(UTC)
            )
        except (ValueError, AttributeError):
            created_at = datetime.now(UTC)

        media = s.get("media") or {}
        assets: list[MediaAsset] = []
        for photo in media.get("photos") or []:
            assets.append(
                MediaAsset(
                    kind=MediaKind.PHOTO,
                    url=photo.get("url", ""),
                    width=photo.get("width"),
                    height=photo.get("height"),
                )
            )
        for video in media.get("videos") or []:
            kind = MediaKind.GIF if video.get("type") == "gif" else MediaKind.VIDEO
            assets.append(
                MediaAsset(
                    kind=kind,
                    url=video.get("url", ""),
                    thumbnail_url=video.get("thumbnail_url"),
                    width=video.get("width"),
                    height=video.get("height"),
                    duration_s=video.get("duration"),
                    bitrate=video.get("bitrate"),
                )
            )

        replying_to = s.get("replying_to")
        if isinstance(replying_to, str):
            is_reply = bool(replying_to)
        else:
            is_reply = bool(replying_to)

        return NormalizedTweet(
            tweet_id=tweet_id,
            author_handle=handle,
            author_id=str(author.get("id") or ""),
            text=s.get("text") or "",
            lang=s.get("lang"),
            created_at=created_at,
            url=s.get("url")
            or (
                f"https://x.com/{handle}/status/{tweet_id}"
                if handle
                else f"https://x.com/i/status/{tweet_id}"
            ),
            is_retweet=bool(s.get("retweeted") or s.get("retweet")),
            is_reply=is_reply,
            is_quote=bool(s.get("quote")),
            media=assets,
            source_fetcher=self.name,
        )
