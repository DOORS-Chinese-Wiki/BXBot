"""结构性过滤：转推 / 回复 / 引用推。"""

from __future__ import annotations

from bxbot.config import FilterConfig
from bxbot.filters.base import FilterContext, FilterRule, FilterVerdict, VerdictKind


class RetweetFilter(FilterRule):
    name = "structural"

    def __init__(self, cfg: FilterConfig):
        self._cfg = cfg

    async def check(self, ctx: FilterContext) -> FilterVerdict:
        t = ctx.tweet
        if self._cfg.skip_retweets and t.is_retweet:
            return FilterVerdict(kind=VerdictKind.DROP, rule=self.name, reason="转推")
        if self._cfg.skip_replies and t.is_reply:
            return FilterVerdict(kind=VerdictKind.DROP, rule=self.name, reason="回复")
        if self._cfg.skip_quotes and t.is_quote:
            return FilterVerdict(kind=VerdictKind.DROP, rule=self.name, reason="引用推")
        return FilterVerdict(kind=VerdictKind.ABSTAIN, rule=self.name)
