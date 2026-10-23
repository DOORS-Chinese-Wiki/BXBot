"""Translator 协议。"""

from __future__ import annotations

from typing import Protocol

from bxbot.models import LLMResult, NormalizedTweet


class TranslateError(Exception):
    """LLM 调用/解析失败（由 pipeline 按 on_failure 策略处理）。"""


class Translator(Protocol):
    async def translate_and_judge(self, tweet: NormalizedTweet) -> LLMResult: ...
    async def healthcheck(self) -> bool: ...
