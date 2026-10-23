"""LLM 过滤：翻译同一次调用中判断广告/NSFW/敏感等（规则链收尾）。"""

from __future__ import annotations

from loguru import logger

from bxbot.config import LLMConfig
from bxbot.filters.base import FilterContext, FilterRule, FilterVerdict, VerdictKind
from bxbot.translate.base import TranslateError, Translator


class LLMFilter(FilterRule):
    name = "llm"

    def __init__(self, translator: Translator, llm_cfg: LLMConfig):
        self._translator = translator
        self._cfg = llm_cfg

    async def check(self, ctx: FilterContext) -> FilterVerdict:
        try:
            result = await self._translator.translate_and_judge(ctx.tweet)
        except TranslateError as e:
            if self._cfg.on_failure == "post_original":
                logger.warning(f"LLM 失败走降级发原文：{e}")
                from bxbot.models import LLMResult

                ctx.llm = LLMResult(
                    translate_zh=ctx.tweet.text,
                    should_sync=True,
                    reason=f"llm_failed_fallback: {e}",
                    title_zh=None,
                    tags=[],
                )
                return FilterVerdict(
                    kind=VerdictKind.PASS, rule=self.name, reason="LLM 降级发原文"
                )
            logger.warning(f"LLM 失败本轮推迟（不消耗次数）：{e}")
            return FilterVerdict(kind=VerdictKind.DEFER, rule=self.name, reason=str(e))

        ctx.llm = result
        if not result.should_sync:
            return FilterVerdict(
                kind=VerdictKind.DROP,
                rule=self.name,
                reason=result.reason or "LLM 判定不同步",
            )
        return FilterVerdict(kind=VerdictKind.PASS, rule=self.name)
