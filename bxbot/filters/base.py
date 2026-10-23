"""过滤规则链：廉价规则先行，LLM 判断收尾。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from loguru import logger

from bxbot.models import LLMResult, NormalizedTweet


class VerdictKind(str, Enum):
    PASS = "pass"  # 明确放行
    DROP = "drop"  # 过滤掉（终态 filtered）
    ABSTAIN = "abstain"  # 本规则不表态
    DEFER = "defer"  # 临时不可用（如 LLM 故障），本轮不处理、下轮再试


@dataclass
class FilterVerdict:
    kind: VerdictKind
    rule: str = ""
    reason: str = ""


@dataclass
class FilterContext:
    """规则间共享的上下文；LLMFilter 把结果挂在这里传给 pipeline，避免二次调用。"""

    tweet: NormalizedTweet
    llm: LLMResult | None = None
    extras: dict = field(default_factory=dict)


class FilterRule(ABC):
    name: str = "rule"

    @abstractmethod
    async def check(self, ctx: FilterContext) -> FilterVerdict: ...


class FilterChain:
    """依次执行规则：DROP/DEFER 立即返回；全 ABSTAIN 视为 PASS。"""

    def __init__(self, rules: list[FilterRule]):
        self._rules = rules

    async def run(self, ctx: FilterContext) -> FilterVerdict:
        for rule in self._rules:
            verdict = await rule.check(ctx)
            if verdict.kind in (VerdictKind.DROP, VerdictKind.DEFER):
                logger.info(
                    f"过滤[{verdict.rule}] {verdict.kind.value}: "
                    f"{ctx.tweet.tweet_id} {verdict.reason}"
                )
                return verdict
        return FilterVerdict(kind=VerdictKind.PASS, rule="chain", reason="")
