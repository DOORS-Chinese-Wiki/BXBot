"""twikit 后端：逆向 X 的 GraphQL web 接口（cookie Client / GuestClient）。"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from loguru import logger

from bxbot.fetchers.base import FetchError
from bxbot.models import MediaAsset, MediaKind, NormalizedTweet

_TW_CREATED_FMT = "%a %b %d %H:%M:%S %z %Y"  # "Wed Oct 10 20:19:24 +0000 2018"


def _attr(obj: Any, name: str, default: Any = None) -> Any:
    """兼容对象属性（含 property）与 dict 取值，属性抛异常时回退 default。"""
    try:
        if isinstance(obj, dict):
            return obj.get(name, default)
        return getattr(obj, name, default)
    except Exception:
        return default


def _parse_created_at(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if isinstance(value, str) and value:
        for fmt in (_TW_CREATED_FMT, "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                return datetime.strptime(value, fmt).astimezone(UTC)
            except ValueError:
                continue
    return datetime.now(UTC)


def _photo_url_orig(url: str) -> str:
    """pbs.twimg.com 图片改写为原图。"""
    if url and "pbs.twimg.com/media/" in url:
        base = url.split("?")[0]
        return f"{base}?name=orig"
    return url


class TwikitFetcher:
    name = "twikit"
    supports_timeline = True

    def __init__(
        self,
        cookies_file: Path,
        proxy: str = "",
        auth_token: str = "",
        ct0: str = "",
    ):
        self._cookies_file = cookies_file
        self._proxy = proxy or None
        self._auth_token = auth_token
        self._ct0 = ct0
        self._client: Any = None

    async def start(self) -> None:
        try:
            import twikit
        except ImportError as e:
            raise FetchError(f"twikit 未安装：{e}") from e

        cookies = self._load_cookies_dict()
        if cookies:
            try:
                client = twikit.Client(language="en-US", proxy=self._proxy)
                client.set_cookies(cookies)
                self._client = client
                logger.info(f"twikit：已加载 cookies（{len(cookies)} 字段）")
                return
            except Exception as e:
                logger.warning(f"twikit cookie 登录失败，尝试 guest：{e}")

        # guest 模式（独立 GuestClient，需 activate）
        try:
            from twikit.guest import GuestClient

            guest = GuestClient(language="en-US", proxy=self._proxy)
            await guest.activate()
            self._client = guest
            logger.info("twikit：guest 模式已激活")
        except Exception as e:
            raise FetchError(
                f"twikit guest 激活失败（{type(e).__name__}: {e}）。"
                f"请运行 python -m bxbot login-x 导入 cookies，或配置 twitter.proxy"
            ) from e

    async def close(self) -> None:
        self._client = None

    # ---- 抓取 ----

    async def fetch_user_timeline(
        self, *, target_handle: str, since_id: str | None, limit: int = 20
    ) -> list[NormalizedTweet]:
        client = self._require_client()
        try:
            user = await client.get_user_by_screen_name(target_handle)
        except Exception as e:
            raise FetchError(f"获取用户 @{target_handle} 失败：{e}") from e
        user_id = _attr(user, "id")
        try:
            raw_list = await client.get_user_tweets(user_id, "Tweets", count=limit)
        except Exception as e:
            raise FetchError(f"拉取 @{target_handle} 时间线失败：{e}") from e

        tweets = [
            self._normalize(t, fallback_handle=target_handle)
            for t in list(raw_list or [])
        ]
        if since_id and since_id != "0":
            tweets = [t for t in tweets if int(t.tweet_id) > int(since_id)]
        tweets.sort(key=lambda t: int(t.tweet_id))
        return tweets[:limit]

    async def fetch_tweet(self, tweet_id: str) -> NormalizedTweet | None:
        client = self._require_client()
        try:
            raw = await client.get_tweet_by_id(tweet_id)
        except Exception as e:
            raise FetchError(f"获取推文 {tweet_id} 失败：{e}") from e
        return self._normalize(raw) if raw else None

    # ---- 归一化 ----

    def _normalize(self, raw: Any, fallback_handle: str = "") -> NormalizedTweet:
        user = _attr(raw, "user") or {}
        handle = _attr(user, "screen_name") or fallback_handle
        tweet_id = str(_attr(raw, "id") or "")
        text = _attr(raw, "text") or ""

        media_assets: list[MediaAsset] = []
        for m in _attr(raw, "media") or []:
            try:
                asset = self._normalize_media(m)
            except Exception as e:
                logger.debug(f"媒体解析失败跳过：{e}")
                asset = None
            if asset:
                media_assets.append(asset)

        return NormalizedTweet(
            tweet_id=tweet_id,
            author_handle=handle,
            author_id=str(_attr(user, "id") or ""),
            text=text,
            lang=_attr(raw, "lang"),
            created_at=_parse_created_at(_attr(raw, "created_at")),
            url=(
                f"https://x.com/{handle}/status/{tweet_id}"
                if handle
                else f"https://x.com/i/status/{tweet_id}"
            ),
            is_retweet=bool(_attr(raw, "retweeted_tweet")),
            is_reply=bool(_attr(raw, "in_reply_to")),
            is_quote=bool(
                _attr(raw, "is_quote_status", False) or _attr(raw, "quoted_tweet")
            ),
            media=media_assets,
            source_fetcher=self.name,
        )

    @staticmethod
    def _normalize_media(m: Any) -> MediaAsset | None:
        mtype = (_attr(m, "type") or type(m).__name__ or "").lower()
        thumb = _attr(m, "media_url")
        width = _attr(m, "width")
        height = _attr(m, "height")

        # 图片：下载地址是 media_url（media_url_https），不是 t.co 短链
        if mtype in ("photo", "image") or type(m).__name__ == "Photo":
            url = thumb or _attr(m, "url") or ""
            return MediaAsset(
                kind=MediaKind.PHOTO,
                url=_photo_url_orig(url),
                thumbnail_url=thumb,
                width=width,
                height=height,
            )

        # 视频/GIF：从 streams() 取最高码率 mp4 直链
        if mtype in ("video", "gif", "animated_gif") or hasattr(m, "streams"):
            duration = _attr(m, "duration_millis")
            duration_s = float(duration) / 1000.0 if duration else None
            best_url, best_bitrate = "", 0
            try:
                streams = m.streams()
            except Exception:
                streams = []
            for s in streams or []:
                s_url = _attr(s, "url") or ""
                s_br = _attr(s, "bitrate") or 0
                ctype = _attr(s, "content_type") or ""
                if ".m3u8" in s_url:
                    continue
                if ".mp4" not in s_url and "mp4" not in ctype:
                    continue
                if s_br >= best_bitrate:
                    best_url, best_bitrate = s_url, s_br
            if not best_url:
                return None
            kind = (
                MediaKind.GIF
                if mtype in ("gif", "animated_gif") or type(m).__name__ == "AnimatedGif"
                else MediaKind.VIDEO
            )
            return MediaAsset(
                kind=kind,
                url=best_url,
                thumbnail_url=thumb,
                width=width,
                height=height,
                duration_s=duration_s,
                bitrate=best_bitrate or None,
            )
        return None

    # ---- 内部 ----

    def _load_cookies_dict(self) -> dict[str, str]:
        import json

        if self._cookies_file.exists():
            try:
                data = json.loads(self._cookies_file.read_text(encoding="utf-8"))
                if isinstance(data, dict) and data:
                    return {str(k): str(v) for k, v in data.items()}
            except Exception as e:
                logger.warning(f"cookies 文件读取失败：{e}")
        if self._auth_token and self._ct0:
            return {"auth_token": self._auth_token, "ct0": self._ct0}
        return {}

    def _require_client(self) -> Any:
        if self._client is None:
            raise FetchError("twikit 未初始化（先调用 start()）")
        return self._client
