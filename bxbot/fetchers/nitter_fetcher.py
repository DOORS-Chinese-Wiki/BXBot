"""Nitter/RSS 后端（预留 stub）：大部分实例已不稳定，默认不启用。"""

from __future__ import annotations

from bxbot.fetchers.base import FetchError
from bxbot.models import NormalizedTweet


class NitterFetcher:
    name = "nitter"
    supports_timeline = True

    def __init__(self, base_url: str = "", proxy: str = ""):
        self._base_url = base_url.rstrip("/") if base_url else ""
        self._proxy = proxy

    async def start(self) -> None:
        if not self._base_url:
            raise FetchError("nitter 后端未配置 base_url（默认禁用）")

    async def close(self) -> None:
        pass

    async def fetch_user_timeline(
        self, *, target_handle: str, since_id: str | None, limit: int = 20
    ) -> list[NormalizedTweet]:
        raise FetchError("nitter 后端暂未实现（仅预留接口）")

    async def fetch_tweet(self, tweet_id: str) -> NormalizedTweet | None:
        raise FetchError("nitter 后端暂未实现（仅预留接口）")
