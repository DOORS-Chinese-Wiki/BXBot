"""关键词黑名单过滤（支持 re: 前缀的正则）。"""

from __future__ import annotations

import re

from bxbot.config import FilterConfig
from bxbot.filters.base import FilterContext, FilterRule, FilterVerdict, VerdictKind


class KeywordFilter(FilterRule):
    name = "keyword"

    def __init__(self, cfg: FilterConfig):
        self._patterns: list[re.Pattern] = []
        for item in cfg.keyword_blacklist:
            if item.startswith("re:"):
                self._patterns.append(re.compile(item[3:], re.IGNORECASE))
            else:
                self._patterns.append(re.compile(re.escape(item), re.IGNORECASE))

    async def check(self, ctx: FilterContext) -> FilterVerdict:
        text = ctx.tweet.text
        for pat in self._patterns:
            if pat.search(text):
                return FilterVerdict(
                    kind=VerdictKind.DROP,
                    rule=self.name,
                    reason=f"命中关键词 /{pat.pattern}/",
                )
        return FilterVerdict(kind=VerdictKind.ABSTAIN, rule=self.name)
