"""视频封面：缩略图下载 → ffmpeg 首帧 → Pillow 占位图，三级回退。"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import httpx
from loguru import logger

from bxbot.models import NormalizedTweet


async def ensure_cover(
    tweet: NormalizedTweet, video_path: Path, out_dir: Path, *, proxy: str = ""
) -> Path:
    """保证产出一张封面图（永不失败：至少有占位图）。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    cover_path = out_dir / "cover.jpg"

    # 1) 推文视频缩略图
    thumb = next((m.thumbnail_url for m in tweet.media if m.thumbnail_url), None)
    if thumb:
        try:
            async with httpx.AsyncClient(
                proxy=proxy or None, timeout=20, follow_redirects=True
            ) as client:
                resp = await client.get(thumb)
                resp.raise_for_status()
                cover_path.write_bytes(resp.content)
                logger.debug("封面：使用视频缩略图")
                return cover_path
        except Exception as e:
            logger.warning(f"缩略图下载失败，尝试 ffmpeg：{e}")

    # 2) ffmpeg 抽首帧（PATH 里有才用）
    if shutil.which("ffmpeg"):
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    "0",
                    "-i",
                    str(video_path),
                    "-frames:v",
                    "1",
                    str(cover_path),
                ],
                check=True,
                capture_output=True,
                timeout=30,
            )
            logger.debug("封面：ffmpeg 抽首帧")
            return cover_path
        except Exception as e:
            logger.warning(f"ffmpeg 抽帧失败，尝试占位图：{e}")

    # 3) Pillow 占位图（16:10）
    _placeholder_cover(tweet, cover_path)
    logger.debug("封面：使用占位图")
    return cover_path


def _placeholder_cover(
    tweet: NormalizedTweet, out_path: Path, size: tuple[int, int] = (1280, 800)
) -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", size, color=(24, 26, 32))
    draw = ImageDraw.Draw(img)
    lines = (tweet.text or tweet.author_handle or "BXBot").splitlines()[:4]
    y = size[1] // 2 - len(lines) * 20
    for line in lines:
        draw.text((60, y), line[:40], fill=(220, 222, 228))
        y += 40
    draw.text((60, size[1] - 60), f"@{tweet.author_handle}", fill=(140, 145, 160))
    img.save(out_path, "JPEG", quality=88)
