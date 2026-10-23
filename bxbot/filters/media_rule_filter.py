"""媒体规则预检：图片数量、视频时长/体积（按元数据预判）。"""

from __future__ import annotations

from bxbot.config import FilterConfig
from bxbot.filters.base import FilterContext, FilterRule, FilterVerdict, VerdictKind
from bxbot.models import MediaKind


class MediaRuleFilter(FilterRule):
    name = "media_rule"

    def __init__(self, cfg: FilterConfig):
        self._cfg = cfg

    async def check(self, ctx: FilterContext) -> FilterVerdict:
        t = ctx.tweet
        photos = [m for m in t.media if m.kind == MediaKind.PHOTO]
        videos = [m for m in t.media if m.kind in (MediaKind.VIDEO, MediaKind.GIF)]

        if len(photos) > self._cfg.max_images:
            # 超出上限不直接杀：标记 extras 供下载阶段截断
            ctx.extras["truncate_images"] = self._cfg.max_images

        for v in videos:
            if v.duration_s and v.duration_s > self._cfg.max_video_s:
                return FilterVerdict(
                    kind=VerdictKind.DROP,
                    rule=self.name,
                    reason=f"视频时长 {v.duration_s:.0f}s 超限 {self._cfg.max_video_s}s",
                )
        return FilterVerdict(kind=VerdictKind.ABSTAIN, rule=self.name)
