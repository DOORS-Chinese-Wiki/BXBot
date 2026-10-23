"""轮询调度：run_once 单轮 / run_forever 常驻。"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass, field

from loguru import logger

from bxbot.config import Config, ensure_runtime_dirs
from bxbot.fetchers import FetcherChain
from bxbot.fetchers.fxtwitter_fetcher import FxTwitterFetcher
from bxbot.fetchers.nitter_fetcher import NitterFetcher
from bxbot.fetchers.twikit_fetcher import TwikitFetcher
from bxbot.fetchers.x_ssr import XSsrFetcher
from bxbot.media import MediaDownloader, purge_orphans
from bxbot.models import NormalizedTweet, TweetStatus
from bxbot.pipeline import BiliRiskError, Pipeline, build_filter_chain
from bxbot.publishers import DryRunPublisher, PublishDispatcher
from bxbot.state import StateStore
from bxbot.translate.openai_compat import OpenAICompatTranslator
from bxbot.utils.win import install_stop_signals

WATERMARK_KEY = "watermark_id"
RISK_UNTIL_KEY = "risk_until"


@dataclass
class RunStats:
    fetched: int = 0
    published: int = 0
    filtered: int = 0
    failed: int = 0
    deferred: int = 0
    notes: list[str] = field(default_factory=list)


def build_fetcher_chain(cfg: Config) -> FetcherChain:
    fetchers = []
    for name in cfg.twitter.backend_order:
        if name == "x_ssr":
            fetchers.append(XSsrFetcher(proxy=cfg.twitter.proxy))
        elif name == "twikit":
            fetchers.append(
                TwikitFetcher(
                    cookies_file=cfg.x_cookies_path,
                    proxy=cfg.twitter.proxy,
                    auth_token=_env("TWITTER_AUTH_TOKEN"),
                    ct0=_env("TWITTER_CT0"),
                )
            )
        elif name == "fxtwitter":
            fetchers.append(FxTwitterFetcher(proxy=cfg.twitter.proxy))
        elif name == "nitter":
            fetchers.append(NitterFetcher())
        else:
            logger.warning(f"未知 fetcher 后端：{name}，忽略")
    return FetcherChain(fetchers)


def _env(key: str) -> str:
    import os

    return os.environ.get(key, "")


async def run_once(
    cfg: Config,
    *,
    dry_run: bool = False,
    tweet_id: str | None = None,
    force: bool = False,
) -> RunStats:
    """执行一轮：（可选）补处理 pending/failed → 拉时间线增量 → 逐条流水线。"""
    ensure_runtime_dirs(cfg)
    store = StateStore(cfg.db_path)
    stats = RunStats()
    chain = build_fetcher_chain(cfg)
    translator = OpenAICompatTranslator.from_config(cfg.llm)
    filters = build_filter_chain(cfg, translator if cfg.filter.llm_enabled else None)
    downloader = MediaDownloader(
        cfg.tmp_dir,
        max_video_mb=cfg.filter.max_video_mb,
        max_images=cfg.filter.max_images,
        proxy=cfg.twitter.proxy,
    )
    if dry_run or cfg.bilibili.dry_run:
        publisher = DryRunPublisher()
    else:
        from bxbot.publishers.bilibili.publisher import BiliPublisher

        publisher = await BiliPublisher.create(cfg)

    pipeline = Pipeline(
        cfg, store, filters, translator, downloader, PublishDispatcher(publisher)
    )
    try:
        await chain.start()

        # 风控熔断窗口内直接跳过本轮发布
        risk_until = float(store.get_meta(RISK_UNTIL_KEY) or 0)
        if time.time() < risk_until:
            stats.notes.append(f"B 站风控熔断中，剩余 {risk_until - time.time():.0f}s")
            return stats

        purge_orphans(cfg.tmp_dir, keep_ids={r.tweet_id for r in store.pending_rows()})

        # 1) 定点单条（调试/回放/人工强制同步）
        if tweet_id:
            t = await chain.fetch_tweet(tweet_id)
            if t is None:
                stats.notes.append(f"未找到推文 {tweet_id}")
            else:
                await _process_one(pipeline, store, cfg, t, stats, dry_run, force)
            return stats

        # 2) 补处理：pending（LLM 故障推迟/中断）+ 可重试 failed
        resume_rows = store.pending_rows() + store.retryable_failed(
            cfg.poll.max_attempts
        )
        for row in resume_rows:
            try:
                t = await chain.fetch_tweet(row.tweet_id)
            except Exception as e:
                logger.warning(f"补处理拉取 {row.tweet_id} 失败：{e}")
                continue
            if t:
                await _process_one(pipeline, store, cfg, t, stats, dry_run)

        # 3) 时间线增量
        since_id = store.get_meta(WATERMARK_KEY)
        tweets = await chain.fetch_user_timeline(
            target_handle=cfg.target.handle,
            since_id=since_id,
            limit=cfg.twitter.page_size,
        )
        stats.fetched = len(tweets)

        if since_id is None:
            # 首轮：只建立水位，不处理历史（产品决策：只同步新推文）
            if tweets:
                store.set_meta(
                    WATERMARK_KEY, max((t.tweet_id for t in tweets), key=int)
                )
            else:
                store.set_meta(WATERMARK_KEY, "0")
            stats.notes.append("首轮启动：已建立水位，不回填历史推文")
            return stats

        for t in tweets:
            await _process_one(pipeline, store, cfg, t, stats, dry_run)
            store.set_meta(WATERMARK_KEY, t.tweet_id)
            if stats.published >= cfg.bilibili.max_publish_per_round:
                stats.notes.append("达到单轮发布上限，剩余推文下轮处理")
                break

        return stats
    finally:
        close_pub = getattr(publisher, "close", None)
        if close_pub is not None:
            try:
                await close_pub()
            except Exception:
                pass
        await chain.close()
        await translator.close()
        store.close()


async def _process_one(
    pipeline: Pipeline,
    store: StateStore,
    cfg: Config,
    tweet: NormalizedTweet,
    stats: RunStats,
    dry_run: bool,
    force: bool = False,
) -> None:
    try:
        outcome = await pipeline.process(tweet, force=force)
    except BiliRiskError as e:
        stats.failed += 1
        cooldown = cfg.bilibili.risk_cooldown_s
        store.set_meta(RISK_UNTIL_KEY, str(time.time() + cooldown))
        logger.error(f"触发 B 站风控，熔断 {cooldown}s：{e}")
        stats.notes.append("触发 B 站风控，本轮终止")
        raise

    if outcome.skipped:
        return  # 已终态跳过：不计数、不等待发布间隔
    if outcome.status == TweetStatus.PUBLISHED:
        stats.published += 1
        if not (dry_run or cfg.bilibili.dry_run):
            gap = cfg.bilibili.publish_gap_seconds
            if gap > 0:
                logger.info(f"发布间隔等待 {gap}s（防风控）")
                await asyncio.sleep(gap)
    elif outcome.status == TweetStatus.FILTERED:
        stats.filtered += 1
    elif outcome.status == TweetStatus.PENDING:
        stats.deferred += 1
    else:
        stats.failed += 1


async def run_forever(cfg: Config, *, dry_run: bool = False) -> None:
    """常驻轮询：每 interval(±10% jitter) 一轮；stop_event 置位后完成当前轮再退出。"""
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    install_stop_signals(loop, stop_event)

    logger.info(
        f"BXBot 启动：@{cfg.target.handle} → B 站"
        f"{'（DRY-RUN）' if dry_run or cfg.bilibili.dry_run else ''}"
        f"，轮询间隔 {cfg.poll.interval_seconds}s"
    )
    while not stop_event.is_set():
        try:
            stats = await run_once(cfg, dry_run=dry_run)
            logger.info(
                f"本轮完成：拉取 {stats.fetched} 发布 {stats.published} "
                f"过滤 {stats.filtered} 失败 {stats.failed} 推迟 {stats.deferred}"
                + (f" | {'; '.join(stats.notes)}" if stats.notes else "")
            )
        except BiliRiskError:
            logger.warning("因风控提前结束本轮，进入熔断等待")
        except Exception as e:
            logger.exception(f"本轮异常：{e}")

        if stop_event.is_set():
            break
        interval = cfg.poll.interval_seconds * random.uniform(0.9, 1.1)
        logger.info(f"休眠 {interval:.0f}s 等待下一轮（Ctrl+C 退出）")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=interval)
        except TimeoutError:
            pass
    logger.info("BXBot 已停止")
