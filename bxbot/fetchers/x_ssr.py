"""X 主页 SSR 抓取后端：解析 x.com 账号页服务端直出的推文 JSON。

原理：x.com 对未登录访客在账号页 HTML 里服务端渲染最近推文
（React Flight 风格 `id:"VHdlZXRSZXN1bHRzOj…"` / `rest_id:"…"` 对象字面量），
不需要事务签名/guest token/官方 API。缺点：单页只有最近几条，无分页。
"""

from __future__ import annotations

import base64
import json
import re
from datetime import UTC, datetime

import httpx

from bxbot.fetchers.base import FetchError
from bxbot.models import MediaAsset, MediaKind, NormalizedTweet
from bxbot.publishers.bilibili.textfmt import expand_tco_links

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# 推文对象标记：id:"<base64，'TweetResults:' 前缀>"
_TWEET_MARKER = re.compile(r'id:"(VHdlZXRSZXN1bHRz[A-Za-z0-9+/=]*)"')
_STR = r'"((?:[^"\\]|\\.)*)"'


def _unescape(s: str) -> str:
    try:
        return json.loads(f'"{s}"')
    except Exception:
        return s


def _decode_tweet_id(b64: str) -> str | None:
    try:
        raw = base64.b64decode(b64 + "==").decode("utf-8", errors="replace")
    except Exception:
        return None
    m = re.search(r"(\d+)$", raw)  # "TweetResults:<digits>"
    return m.group(1) if m else None


def extract_tweets_from_html(
    html: str, fallback_handle: str = ""
) -> list[NormalizedTweet]:
    """从账号页/状态页 HTML 提取推文列表（按 tweet_id 去重）。"""
    markers = list(_TWEET_MARKER.finditer(html))
    out: list[NormalizedTweet] = []
    seen: set[str] = set()

    for i, m in enumerate(markers):
        start = m.start()
        end = (
            markers[i + 1].start()
            if i + 1 < len(markers)
            else min(start + 30000, len(html))
        )
        block = html[start:end]

        # 推文 ID：marker 的 base64 解码，失败退回紧随的 rest_id
        tweet_id = _decode_tweet_id(m.group(1))
        if not tweet_id:
            rm = re.search(rf"rest_id:{_STR}", block)
            tweet_id = _unescape(rm.group(1)) if rm else ""
        if not tweet_id or not tweet_id.isdigit() or tweet_id in seen:
            continue

        # 正文（必须有）
        text_m = re.search(rf"full_text:{_STR}", block)
        if not text_m:
            continue
        text = _unescape(text_m.group(1))

        # t.co 短链 → 真实链接（entities.urls：expanded_url 与 url 同实体相邻）
        url_entities: dict[str, str] = {}
        for em in re.finditer(rf"expanded_url:{_STR}", block):
            expanded = _unescape(em.group(1))
            window = block[em.end() : em.end() + 250]
            um = re.search(r'url:"(https://t\.co/[^"]+)"', window)
            if um:
                url_entities[_unescape(um.group(1))] = expanded
        text = expand_tco_links(text, url_entities)

        # 时间：created_at_ms（毫秒时间戳）
        created_at = datetime.now(UTC)
        ts_m = re.search(r"created_at_ms:(\d{10,13})", block)
        if ts_m:
            ts = int(ts_m.group(1))
            if ts > 10**12:
                ts //= 1000
            created_at = datetime.fromtimestamp(ts, tz=UTC)

        # 作者：块内首个 screen_name（core.user_results 字母序排在 entities.mentions 之前）
        handle = fallback_handle
        sn_m = re.search(rf"screen_name:{_STR}", block)
        if sn_m:
            handle = _unescape(sn_m.group(1)) or fallback_handle

        # 图片：只认 /media/ 路径（视频缩略图走 thumb，不当图片）
        photos: list[MediaAsset] = []
        for url in re.findall(rf"media_url_https:{_STR}", block):
            url = _unescape(url)
            if "pbs.twimg.com/media/" in url:
                base = url.split("?")[0]
                photos.append(MediaAsset(kind=MediaKind.PHOTO, url=f"{base}?name=orig"))

        # 视频：mp4 直链取最高码率（对象键字母序，bitrate 在 url 前，回看 80 字符）
        thumb = None
        for u in re.findall(rf"media_url_https:{_STR}", block):
            u = _unescape(u)
            if (
                "amplify_video_thumb" in u
                or "ext_tw_video" in u
                or "tweet_video_thumb" in u
            ):
                thumb = u
                break
        best_mp4, best_br = "", 0
        for vm in re.finditer(rf"url:{_STR}", block):
            url = _unescape(vm.group(1))
            if not (url.startswith("https://video.twimg.com/") and ".mp4" in url):
                continue
            lookback = block[max(0, vm.start() - 80) : vm.start()]
            br_m = re.findall(r"bitrate:(\d+)", lookback)
            br = int(br_m[-1]) if br_m else 0
            if br >= best_br:
                best_mp4, best_br = url, br

        media = list(photos)
        if best_mp4:
            is_gif = 'type:"animated_gif"' in block
            media.append(
                MediaAsset(
                    kind=MediaKind.GIF if is_gif else MediaKind.VIDEO,
                    url=best_mp4,
                    thumbnail_url=thumb,
                    duration_s=None,
                    bitrate=best_br or None,
                )
            )

        seen.add(tweet_id)
        out.append(
            NormalizedTweet(
                tweet_id=tweet_id,
                author_handle=handle,
                text=text,
                created_at=created_at,
                url=(
                    f"https://x.com/{handle}/status/{tweet_id}"
                    if handle
                    else f"https://x.com/i/status/{tweet_id}"
                ),
                is_retweet="retweeted_status_result" in block,
                is_reply=bool(re.search(r'in_reply_to_status_id_str:"\d+"', block)),
                is_quote="quoted_status_result" in block,
                media=media,
                url_entities=url_entities,
                source_fetcher="x_ssr",
            )
        )

    out.sort(key=lambda t: int(t.tweet_id))
    return out


class XSsrFetcher:
    """抓取 x.com 页面 HTML 并解析内嵌推文（无需登录/签名）。"""

    name = "x_ssr"
    supports_timeline = True

    def __init__(self, proxy: str = "", timeout_s: float = 25.0):
        self._proxy = proxy or None
        self._timeout = timeout_s
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        self._client = httpx.AsyncClient(
            proxy=self._proxy,
            timeout=httpx.Timeout(self._timeout),
            follow_redirects=True,
            headers={
                "User-Agent": _UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def fetch_user_timeline(
        self, *, target_handle: str, since_id: str | None, limit: int = 20
    ) -> list[NormalizedTweet]:
        assert self._client is not None
        try:
            resp = await self._client.get(f"https://x.com/{target_handle}")
            resp.raise_for_status()
        except Exception as e:
            raise FetchError(
                f"x_ssr 拉取 @{target_handle} 页面失败：{type(e).__name__}: {e}"
            ) from e

        tweets = extract_tweets_from_html(resp.text, fallback_handle=target_handle)
        if not tweets:
            raise FetchError(
                f"x_ssr 未能从 @{target_handle} 页面解析出推文（页面结构可能变更）"
            )
        if since_id and since_id != "0":
            tweets = [t for t in tweets if int(t.tweet_id) > int(since_id)]
        return tweets[:limit]

    async def fetch_tweet(self, tweet_id: str) -> NormalizedTweet | None:
        assert self._client is not None
        try:
            resp = await self._client.get(f"https://x.com/i/status/{tweet_id}")
            resp.raise_for_status()
        except Exception as e:
            raise FetchError(
                f"x_ssr 拉取推文 {tweet_id} 页面失败：{type(e).__name__}: {e}"
            ) from e
        tweets = extract_tweets_from_html(resp.text)
        for t in tweets:
            if t.tweet_id == tweet_id:
                return t
        return tweets[0] if tweets else None
