"""临时媒体目录清理。"""

from __future__ import annotations

import shutil
from pathlib import Path

from loguru import logger


def purge_tweet_dir(tmp_root: Path, tweet_id: str) -> None:
    d = tmp_root / tweet_id
    if d.exists():
        shutil.rmtree(d, ignore_errors=True)


def purge_orphans(tmp_root: Path, keep_ids: set[str] | None = None) -> None:
    """启动时清理历史遗留目录（keep_ids 里的一律保留）。"""
    if not tmp_root.exists():
        return
    keep = keep_ids or set()
    for child in tmp_root.iterdir():
        if child.is_dir() and child.name not in keep:
            shutil.rmtree(child, ignore_errors=True)
            logger.debug(f"清理临时目录 {child.name}")
