"""日志：控制台 + 按大小轮转的文件日志。"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


def setup_logging(logs_dir: Path, level: str = "INFO") -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}",
    )
    logger.add(
        str(logs_dir / "bxbot.log"),
        level=level,
        rotation="10 MB",
        retention=7,
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {name}:{function}:{line} | {message}",
    )
