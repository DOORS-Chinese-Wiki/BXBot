"""媒体下载：图片/视频落盘，mp4 清晰度选择，体积预检。"""

from __future__ import annotations

from pathlib import Path

import httpx
from loguru import logger

from bxbot.models import MediaAsset, MediaKind, NormalizedTweet


class MediaDownloadError(Exception):
    pass


class MediaDownloader:
    def __init__(
        self,
        tmp_root: Path,
        *,
        max_video_mb: int = 512,
        max_images: int = 9,
        timeout_s: float = 120.0,
        proxy: str = "",
        max_retries: int = 3,
    ):
        self._tmp_root = tmp_root
        self._max_video_bytes = max_video_mb * 1024 * 1024
        self._max_images = max_images
        self._timeout = timeout_s
        self._proxy = proxy or None
        self._max_retries = max_retries

    async def download_tweet_media(
        self, tweet: NormalizedTweet, *, truncate_images: int | None = None
    ) -> list[Path]:
        """下载推文媒体到 data/tmp/<tweet_id>/，返回本地路径列表（按序号命名）。"""
        out_dir = self._tmp_root / tweet.tweet_id
        out_dir.mkdir(parents=True, exist_ok=True)

        kind = tweet.media_kind
        if kind in (MediaKind.VIDEO, MediaKind.GIF):
            asset = self.select_best_mp4(tweet.media)
            if asset is None:
                raise MediaDownloadError("没有可用的 mp4 直链（仅 HLS？）")
            path = out_dir / "video.mp4"
            await self._download_to(asset.url, path)
            return [path]
        if kind == MediaKind.MIXED:
            # 混合推文走视频优先（图片保留在推文语境里，不再下载）
            asset = self.select_best_mp4(tweet.media)
            if asset is None:
                raise MediaDownloadError("混合推文没有可用的 mp4 直链")
            path = out_dir / "video.mp4"
            await self._download_to(asset.url, path)
            return [path]
        if kind == MediaKind.PHOTO:
            photos = [m for m in tweet.media if m.kind == MediaKind.PHOTO]
            limit = truncate_images or self._max_images
            if len(photos) > limit:
                logger.info(f"图片 {len(photos)} 张超限，截取前 {limit} 张")
                photos = photos[:limit]
            paths: list[Path] = []
            for i, asset in enumerate(photos):
                suffix = _guess_suffix(asset.url)
                path = out_dir / f"image_{i:02d}{suffix}"
                try:
                    await self._download_to(asset.url, path)
                    paths.append(path)
                except Exception as e:
                    logger.warning(f"图片下载失败跳过 {asset.url}: {e}")
            return paths
        return []

    def select_best_mp4(self, assets: list[MediaAsset]) -> MediaAsset | None:
        """多个清晰度候选：只取 .mp4 直链，≤ 体积上限里码率最高者。"""
        candidates = [
            a
            for a in assets
            if a.kind in (MediaKind.VIDEO, MediaKind.GIF)
            and ".mp4" in a.url
            and ".m3u8" not in a.url
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda a: a.bitrate or 0, reverse=True)
        return candidates[0]

    # ---- 内部 ----

    async def _download_to(self, url: str, path: Path) -> None:
        if path.exists() and path.stat().st_size > 0:
            return
        last_err: Exception | None = None
        async with httpx.AsyncClient(
            proxy=self._proxy,
            timeout=httpx.Timeout(self._timeout),
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BXBot/0.1"
            },
        ) as client:
            for attempt in range(1, self._max_retries + 1):
                try:
                    async with client.stream("GET", url) as resp:
                        resp.raise_for_status()
                        total = resp.headers.get("Content-Length")
                        if total and int(total) > self._max_video_bytes:
                            raise MediaDownloadError(
                                f"文件 {int(total) / 1024 / 1024:.1f}MB 超过上限"
                            )
                        tmp = path.with_suffix(path.suffix + ".part")
                        size = 0
                        with open(tmp, "wb") as f:
                            async for chunk in resp.aiter_bytes(1 << 16):
                                size += len(chunk)
                                if size > self._max_video_bytes:
                                    f.close()
                                    tmp.unlink(missing_ok=True)
                                    raise MediaDownloadError("下载超体积上限")
                                f.write(chunk)
                        tmp.replace(path)
                        logger.debug(f"已下载 {path.name} ({size / 1024:.0f}KB)")
                        return
                except MediaDownloadError:
                    raise
                except Exception as e:
                    last_err = e
                    logger.warning(
                        f"下载失败（{attempt}/{self._max_retries}）{url}: {e}"
                    )
        raise MediaDownloadError(f"下载失败：{url} -> {last_err}")


def _guess_suffix(url: str) -> str:
    clean = url.split("?")[0]
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if clean.lower().endswith(ext):
            return ext
    return ".jpg"
