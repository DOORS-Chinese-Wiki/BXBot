"""单条推文的阶段编排：过滤 → 翻译/判断 → 媒体 → 发布 → 状态落库。"""

from __future__ import annotations

from dataclasses import dataclass

from loguru import logger

from bxbot.config import Config
from bxbot.filters import (
    FilterChain,
    FilterContext,
    FilterVerdict,
    KeywordFilter,
    LLMFilter,
    MediaRuleFilter,
    RetweetFilter,
    VerdictKind,
)
from bxbot.media import MediaDownloader, ensure_cover, purge_tweet_dir
from bxbot.models import (
    LLMResult,
    MediaKind,
    NormalizedTweet,
    PublishBundle,
    TweetStatus,
)
from bxbot.publishers import PublishDispatcher
from bxbot.publishers.bilibili.textfmt import (
    bili_topics_suffix,
    extract_hashtags,
    make_video_title,
    render_body,
    strip_hashtags,
)
from bxbot.state import StateStore
from bxbot.translate.base import Translator


class BiliRiskError(Exception):
    """B 站风控类错误：停止本轮发布并熔断。"""


class BiliContentRejected(Exception):
    """B 站内容审核不通过（敏感词等）：终态 filtered，不重试。"""


@dataclass
class ProcessOutcome:
    status: TweetStatus
    reason: str = ""
    skipped: bool = False  # 因已终态而跳过（不计入发布/失败统计）


class Pipeline:
    def __init__(
        self,
        cfg: Config,
        store: StateStore,
        filters: FilterChain,
        translator: Translator | None,
        downloader: MediaDownloader,
        dispatcher: PublishDispatcher,
    ):
        self._cfg = cfg
        self._store = store
        self._filters = filters
        self._translator = translator
        self._downloader = downloader
        self._dispatcher = dispatcher

    async def process(
        self, tweet: NormalizedTweet, *, force: bool = False
    ) -> ProcessOutcome:
        """处理单条推文；任何异常不外抛（BiliRiskError 除外），状态落库。"""
        tid = tweet.tweet_id
        row = self._store.get(tid)
        if (
            row
            and row.status in (TweetStatus.PUBLISHED.value, TweetStatus.FILTERED.value)
            and not force
        ):
            logger.info(f"推文 {tid} 已终态（{row.status}），跳过")
            return ProcessOutcome(TweetStatus(row.status), "已终态，跳过", skipped=True)
        if row is None and not self._store.try_begin(tid):
            return ProcessOutcome(TweetStatus.PENDING, "并发插入，跳过")

        try:
            return await self._run_stages(tweet, force=force)
        except BiliRiskError:
            self._store.mark(
                tid,
                TweetStatus.FAILED,
                error="B站风控",
                media_kind=tweet.media_kind.value,
                inc_attempt=True,
            )
            raise
        except BiliContentRejected as e:
            self._store.mark(
                tid,
                TweetStatus.FILTERED,
                reason=f"bilibili_rejected: {e}",
                media_kind=tweet.media_kind.value,
            )
            return ProcessOutcome(TweetStatus.FILTERED, f"内容审核不通过：{e}")
        except Exception as e:
            logger.exception(f"处理推文 {tid} 失败：{e}")
            self._store.mark(
                tid,
                TweetStatus.FAILED,
                error=str(e),
                media_kind=tweet.media_kind.value,
                inc_attempt=True,
            )
            return ProcessOutcome(TweetStatus.FAILED, str(e))

    async def _run_stages(
        self, tweet: NormalizedTweet, *, force: bool
    ) -> ProcessOutcome:
        tid = tweet.tweet_id

        # 1) 过滤链（LLMFilter 在链尾会产出 ctx.llm）
        ctx = FilterContext(tweet=tweet)
        if force:
            # 人工强制同步：不做内容过滤，但保留 LLM 翻译（失败则降级原文）
            logger.info(f"FORCE 模式：跳过过滤链 {tid}")
            ctx.llm = None
            if self._translator is not None:
                try:
                    ctx.llm = await self._translator.translate_and_judge(tweet)
                except Exception as e:
                    logger.warning(f"FORCE 模式 LLM 翻译失败降级原文：{e}")
            if ctx.llm is None:
                ctx.llm = LLMResult(translate_zh=tweet.text, should_sync=True)
            else:
                ctx.llm = ctx.llm.model_copy(update={"should_sync": True, "reason": ""})
            verdict = FilterVerdict(kind=VerdictKind.PASS, rule="force")
        else:
            verdict = await self._filters.run(ctx)
        if verdict.kind == VerdictKind.DEFER:
            # LLM 临时故障：保持 pending，不消耗 attempt
            return ProcessOutcome(TweetStatus.PENDING, f"推迟：{verdict.reason}")
        if verdict.kind == VerdictKind.DROP:
            self._store.mark(
                tid,
                TweetStatus.FILTERED,
                reason=f"{verdict.rule}: {verdict.reason}",
                media_kind=tweet.media_kind.value,
            )
            return ProcessOutcome(TweetStatus.FILTERED, verdict.reason)

        if ctx.llm is None:
            # 未启用 LLM 过滤时也要有译文字段
            ctx.llm = LLMResult(translate_zh=tweet.text, should_sync=True)
        llm = ctx.llm

        # 2) 媒体下载（视频失败=整条下轮重试；图片0张成功=降级文字动态）
        media_files = []
        if tweet.media_kind != MediaKind.NONE:
            media_files = await self._downloader.download_tweet_media(
                tweet, truncate_images=ctx.extras.get("truncate_images")
            )
            if not media_files and tweet.media_kind == MediaKind.PHOTO:
                logger.warning(f"{tid} 图片全部下载失败，降级为文字动态")

        # 3) 封面（仅视频稿件需要）
        cover_path = None
        if media_files and tweet.media_kind in (
            MediaKind.VIDEO,
            MediaKind.GIF,
            MediaKind.MIXED,
        ):
            cover_path = await ensure_cover(
                tweet,
                media_files[0],
                self._cfg.tmp_dir / tid,
                proxy=self._cfg.twitter.proxy,
            )

        # 4) 排版与发布（hashtag → B 站标签/话题，不从正文残留）
        hashtags = extract_hashtags(tweet.text)
        translate_clean = strip_hashtags(llm.translate_zh)
        original_clean = strip_hashtags(tweet.text)
        body_base = render_body(
            translate_clean,
            original_clean,
            tweet.url,
            mode=self._cfg.translate.mode,
            always_include_source_link=self._cfg.translate.always_include_source_link,
            max_len=self._cfg.bilibili.desc_max_len,
        )
        # 动态正文：末尾追加 B 站话题格式 #tag#（预算内）
        body = body_base
        topics = bili_topics_suffix(hashtags)
        if topics:
            suffix = "\n\n" + topics
            if len(body) + len(suffix) <= self._cfg.bilibili.desc_max_len:
                body += suffix

        title = (llm.title_zh or "").strip() or make_video_title(
            translate_clean, tweet.author_handle
        )
        # 标签：配置默认 + 推文 hashtag + LLM 生成（B 站 tag 上限 10 个）
        tags = _dedupe_tags(self._cfg.bilibili.tags + hashtags + llm.tags, limit=10)

        bundle = PublishBundle(
            tweet=tweet,
            llm=llm,
            text_final=body,
            desc_final=body_base,
            title=title,
            tags=tags,
            tid=self._cfg.bilibili.tid,
            media_files=media_files,
            cover_path=cover_path,
        )
        result = await self._dispatcher.publish(bundle)
        if not result.ok:
            raise RuntimeError(result.error or "发布失败")

        import json

        self._store.mark(
            tid,
            TweetStatus.PUBLISHED,
            reason=result.kind,
            media_kind=tweet.media_kind.value,
            result_json=json.dumps(
                {
                    "bvid": result.bvid,
                    "dynamic_id": result.dynamic_id,
                    "dyn_rid": result.dyn_rid,
                    "kind": result.kind,
                },
                ensure_ascii=False,
            ),
        )
        purge_tweet_dir(self._cfg.tmp_dir, tid)
        return ProcessOutcome(TweetStatus.PUBLISHED, result.kind)


def _dedupe_tags(tags: list[str], limit: int = 12) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        t = t.strip().lstrip("#")
        key = t.lower()
        if t and key not in seen and len(t) <= 20:
            seen.add(key)
            out.append(t)
        if len(out) >= limit:
            break
    return out


def build_filter_chain(cfg: Config, translator: Translator | None) -> FilterChain:
    """按配置组装过滤规则链（LLM 判断在链尾）。"""
    rules = [
        RetweetFilter(cfg.filter),
        KeywordFilter(cfg.filter),
        MediaRuleFilter(cfg.filter),
    ]
    if cfg.filter.llm_enabled and translator is not None:
        rules.append(LLMFilter(translator, cfg.llm))
    return FilterChain(rules)
