"""Fetcher 协议与多后端降级链（粘滞 + 熔断）。"""

from __future__ import annotations

import time
from typing import Protocol

from loguru import logger

from bxbot.models import NormalizedTweet


class FetchError(Exception):
    """抓取失败（网络/限流/会话失效等），可由下一后端接手。"""


class Fetcher(Protocol):
    name: str
    supports_timeline: bool

    async def start(self) -> None: ...
    async def close(self) -> None: ...

    async def fetch_user_timeline(
        self, *, target_handle: str, since_id: str | None, limit: int = 20
    ) -> list[NormalizedTweet]: ...

    async def fetch_tweet(self, tweet_id: str) -> NormalizedTweet | None: ...


class FetcherChain:
    """按序尝试各后端；成功者本进程内粘滞优先；连续失败 N 次熔断一段时间。"""

    def __init__(
        self,
        fetchers: list[Fetcher],
        sticky_fail_threshold: int = 3,
        cooldown_s: float = 600.0,
    ):
        self._fetchers = fetchers
        self._threshold = sticky_fail_threshold
        self._cooldown_s = cooldown_s
        self._sticky: str | None = None
        self._fails: dict[str, int] = {}
        self._open_until: dict[str, float] = {}

    def _ordered(self) -> list[Fetcher]:
        names = [f.name for f in self._fetchers]
        ordered = list(self._fetchers)
        if self._sticky in names:
            ordered.sort(key=lambda f: 0 if f.name == self._sticky else 1)
        return ordered

    def _available(self) -> list[Fetcher]:
        now = time.monotonic()
        return [f for f in self._ordered() if self._open_until.get(f.name, 0.0) <= now]

    def _record_result(self, name: str, ok: bool) -> None:
        if ok:
            self._sticky = name
            self._fails[name] = 0
            self._open_until.pop(name, None)
        else:
            self._fails[name] = self._fails.get(name, 0) + 1
            if self._fails[name] >= self._threshold:
                self._open_until[name] = time.monotonic() + self._cooldown_s
                self._fails[name] = 0
                logger.warning(
                    f"Fetcher[{name}] 连续失败 {self._threshold} 次，熔断 {self._cooldown_s:.0f}s"
                )

    async def start(self) -> None:
        for f in self._fetchers:
            try:
                await f.start()
            except Exception as e:
                logger.warning(f"Fetcher[{f.name}] 启动失败：{e}")
                self._open_until[f.name] = time.monotonic() + self._cooldown_s

    async def close(self) -> None:
        for f in self._fetchers:
            try:
                await f.close()
            except Exception:
                pass

    async def fetch_user_timeline(
        self, *, target_handle: str, since_id: str | None, limit: int = 20
    ) -> list[NormalizedTweet]:
        errors: list[str] = []
        for f in self._available():
            if not f.supports_timeline:
                continue
            try:
                tweets = await f.fetch_user_timeline(
                    target_handle=target_handle, since_id=since_id, limit=limit
                )
                self._record_result(f.name, True)
                return tweets
            except Exception as e:
                self._record_result(f.name, False)
                errors.append(f"{f.name}: {e}")
                logger.warning(f"Fetcher[{f.name}] 时间线失败，尝试降级：{e}")
        raise FetchError(
            "所有可用后端均失败：" + "; ".join(errors) if errors else "无可用后端"
        )

    async def fetch_tweet(self, tweet_id: str) -> NormalizedTweet | None:
        errors: list[str] = []
        for f in self._available():
            try:
                tweet = await f.fetch_tweet(tweet_id)
                if tweet is not None:
                    self._record_result(f.name, True)
                    return tweet
                # 该后端没找到（页面无此推文），继续尝试下一后端
            except Exception as e:
                self._record_result(f.name, False)
                errors.append(f"{f.name}: {e}")
                logger.warning(f"Fetcher[{f.name}] 单条获取失败，尝试降级：{e}")
        if errors:
            raise FetchError("所有可用后端均失败：" + "; ".join(errors))
        return None
