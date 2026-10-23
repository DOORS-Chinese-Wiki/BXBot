"""核心逻辑单元测试（无网络）：排版、状态库、LLM 解析、过滤链、流水线 dry-run。"""

from __future__ import annotations

import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from bxbot.config import Config
from bxbot.filters import FilterChain, FilterContext, VerdictKind
from bxbot.models import LLMResult, MediaAsset, MediaKind, NormalizedTweet, TweetStatus
from bxbot.pipeline import Pipeline, _dedupe_tags
from bxbot.publishers import DryRunPublisher, PublishDispatcher
from bxbot.publishers.bilibili.textfmt import make_video_title, render_body
from bxbot.state import StateStore
from bxbot.translate.openai_compat import _parse_llm_json


def make_tweet(**kw) -> NormalizedTweet:
    base = dict(
        tweet_id="1234567890",
        author_handle="testuser",
        text="Hello world! This is a test tweet.",
        lang="en",
        created_at=datetime.now(UTC),
        url="https://x.com/testuser/status/1234567890",
    )
    base.update(kw)
    return NormalizedTweet(**base)


class TestTextFmt(unittest.TestCase):
    def test_both_mode(self):
        body = render_body("你好世界", "Hello", "https://x.com/u/status/1", mode="both")
        self.assertIn("你好世界", body)
        self.assertIn("——原推——", body)
        self.assertIn("Hello", body)
        self.assertIn("https://x.com/u/status/1", body)

    def test_translated_only_keeps_link(self):
        body = render_body(
            "你好", "Hello", "https://x.com/u/status/1", mode="translated_only"
        )
        self.assertNotIn("Hello", body)
        self.assertIn("https://x.com/u/status/1", body)

    def test_truncation_keeps_link(self):
        body = render_body(
            "长" * 3000, "orig", "https://x.com/u/status/1", mode="both", max_len=500
        )
        self.assertLessEqual(len(body), 500)
        self.assertIn("https://x.com/u/status/1", body)

    def test_video_title(self):
        self.assertEqual(make_video_title("第一行标题\n第二行"), "第一行标题")
        self.assertTrue(make_video_title("   ", "user").startswith("@user"))


class TestStateStore(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = StateStore(Path(self._tmp.name) / "state.db")

    def tearDown(self):
        self.store.close()
        self._tmp.cleanup()

    def test_dedup(self):
        self.assertTrue(self.store.try_begin("1"))
        self.assertFalse(self.store.try_begin("1"))

    def test_state_machine(self):
        self.store.try_begin("1")
        self.store.mark("1", TweetStatus.FAILED, error="boom", inc_attempt=True)
        row = self.store.get("1")
        self.assertEqual(row.status, "failed")
        self.assertEqual(row.attempt_count, 1)
        retryable = self.store.retryable_failed(max_attempts=3)
        self.assertEqual(len(retryable), 1)
        self.store.mark("1", TweetStatus.PUBLISHED, result_json='{"bvid":"BV1"}')
        self.assertEqual(len(self.store.retryable_failed(3)), 0)

    def test_meta_and_pending(self):
        self.assertIsNone(self.store.get_meta("watermark_id"))
        self.store.set_meta("watermark_id", "999")
        self.assertEqual(self.store.get_meta("watermark_id"), "999")
        self.store.try_begin("2")
        self.assertEqual([r.tweet_id for r in self.store.pending_rows()], ["2"])


class TestLLMParse(unittest.TestCase):
    def test_plain_json(self):
        self.assertEqual(_parse_llm_json('{"a": 1}'), {"a": 1})

    def test_fenced_json(self):
        data = _parse_llm_json('```json\n{"translate": "好", "should_sync": true}\n```')
        self.assertTrue(data["should_sync"])

    def test_json_with_noise(self):
        data = _parse_llm_json(
            '结果如下：{"should_sync": false, "reason": "广告"} 以上。'
        )
        self.assertFalse(data["should_sync"])


class TestHashtags(unittest.TestCase):
    def test_extract(self):
        from bxbot.publishers.bilibili.textfmt import extract_hashtags

        self.assertEqual(
            extract_hashtags("stay tuned ^_^ #RobloxDoors and #DOORS!"),
            ["RobloxDoors", "DOORS"],
        )
        self.assertEqual(extract_hashtags("#a then #A dedup"), ["a"])
        self.assertEqual(extract_hashtags("#中文标签 too"), ["中文标签"])
        self.assertEqual(extract_hashtags("no tags"), [])

    def test_extract_ignores_url_anchor(self):
        from bxbot.publishers.bilibili.textfmt import extract_hashtags

        self.assertEqual(extract_hashtags("see https://x.com/path#anchor here"), [])

    def test_strip(self):
        from bxbot.publishers.bilibili.textfmt import strip_hashtags

        self.assertEqual(strip_hashtags("tune in #RobloxDoors now"), "tune in now")
        self.assertEqual(strip_hashtags("start #tag"), "start")
        self.assertEqual(strip_hashtags("no tags here"), "no tags here")

    def test_topics_suffix(self):
        from bxbot.publishers.bilibili.textfmt import bili_topics_suffix

        self.assertEqual(bili_topics_suffix(["A", "B"]), "#A# #B#")
        self.assertEqual(bili_topics_suffix([]), "")

    def test_tags_limit_10(self):
        from bxbot.pipeline import _dedupe_tags

        self.assertEqual(len(_dedupe_tags([f"t{i}" for i in range(15)], limit=10)), 10)


class TestExpandTco(unittest.TestCase):
    def test_expand_external(self):
        from bxbot.publishers.bilibili.textfmt import expand_tco_links

        out = expand_tco_links(
            "check it out https://t.co/9xTe22SEsI",
            {"https://t.co/9xTe22SEsI": "http://doorsgame.wiki"},
        )
        self.assertEqual(out, "check it out http://doorsgame.wiki")

    def test_remove_pic_links(self):
        from bxbot.publishers.bilibili.textfmt import expand_tco_links

        out = expand_tco_links(
            "cute pic https://t.co/AbCdEfG",
            {"https://t.co/AbCdEfG": "https://pic.twitter.com/AbCdEfG"},
        )
        self.assertEqual(out, "cute pic")

    def test_remove_x_photo_page(self):
        from bxbot.publishers.bilibili.textfmt import expand_tco_links

        out = expand_tco_links(
            "look https://t.co/xYz12345 https://t.co/keepMe",
            {
                "https://t.co/xYz12345": "https://x.com/DoorsWiki/status/123/photo/1",
                "https://t.co/keepMe": "https://doorsgame.wiki/",
            },
        )
        self.assertEqual(out, "look https://doorsgame.wiki/")

    def test_no_entities_noop(self):
        from bxbot.publishers.bilibili.textfmt import expand_tco_links

        self.assertEqual(expand_tco_links("plain text", None), "plain text")


class TestHelpers(unittest.TestCase):
    def test_dedupe_tags(self):
        self.assertEqual(_dedupe_tags(["A", "a", "#B", "B", ""]), ["A", "B"])
        self.assertEqual(len(_dedupe_tags([f"t{i}" for i in range(20)])), 12)


class TestFilterChain(unittest.IsolatedAsyncioTestCase):
    async def test_drop_and_defer(self):
        from bxbot.filters.base import FilterRule, FilterVerdict

        class DropRule(FilterRule):
            name = "drop"

            async def check(self, ctx):
                return FilterVerdict(kind=VerdictKind.DROP, rule=self.name, reason="no")

        class DeferRule(FilterRule):
            name = "defer"

            async def check(self, ctx):
                return FilterVerdict(
                    kind=VerdictKind.DEFER, rule=self.name, reason="later"
                )

        class PassRule(FilterRule):
            name = "pass"

            async def check(self, ctx):
                return FilterVerdict(kind=VerdictKind.PASS, rule=self.name)

        tweet = make_tweet()
        chain = FilterChain([DropRule(), PassRule()])
        v = await chain.run(FilterContext(tweet=tweet))
        self.assertEqual(v.kind, VerdictKind.DROP)

        chain = FilterChain([DeferRule()])
        v = await chain.run(FilterContext(tweet=tweet))
        self.assertEqual(v.kind, VerdictKind.DEFER)

        chain = FilterChain([PassRule()])
        v = await chain.run(FilterContext(tweet=tweet))
        self.assertEqual(v.kind, VerdictKind.PASS)


class StubTranslator:
    def __init__(self, result: LLMResult | None = None, fail: bool = False):
        self._result = result or LLMResult(
            translate_zh="译文", should_sync=True, title_zh="标题", tags=["tag1"]
        )
        self._fail = fail
        self.calls = 0

    async def translate_and_judge(self, tweet):
        self.calls += 1
        if self._fail:
            from bxbot.translate.base import TranslateError

            raise TranslateError("stub failure")
        return self._result

    async def healthcheck(self):
        return True


class TestPipeline(unittest.IsolatedAsyncioTestCase):
    def _cfg(self, tmp: Path) -> Config:
        cfg = Config.model_validate(
            {
                "target": {"handle": "testuser"},
                "bilibili": {"dry_run": True, "publish_gap_seconds": 0},
                "filter": {"llm_enabled": True},
            }
        )
        cfg.project_root = tmp
        return cfg

    async def test_publish_text_dry_run(self):
        from bxbot.media import MediaDownloader
        from bxbot.pipeline import build_filter_chain

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cfg = self._cfg(tmp_path)
            store = StateStore(cfg.db_path)
            translator = StubTranslator()
            pipeline = Pipeline(
                cfg,
                store,
                build_filter_chain(cfg, translator),
                translator,
                MediaDownloader(cfg.tmp_dir),
                PublishDispatcher(DryRunPublisher()),
            )
            outcome = await pipeline.process(make_tweet())
            self.assertEqual(outcome.status, TweetStatus.PUBLISHED)
            row = store.get("1234567890")
            self.assertEqual(row.status, "published")
            self.assertEqual(translator.calls, 1)
            store.close()

    async def test_llm_filter_drop(self):
        from bxbot.media import MediaDownloader
        from bxbot.pipeline import build_filter_chain

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cfg = self._cfg(tmp_path)
            store = StateStore(cfg.db_path)
            translator = StubTranslator(
                LLMResult(translate_zh="x", should_sync=False, reason="广告")
            )
            pipeline = Pipeline(
                cfg,
                store,
                build_filter_chain(cfg, translator),
                translator,
                MediaDownloader(cfg.tmp_dir),
                PublishDispatcher(DryRunPublisher()),
            )
            outcome = await pipeline.process(make_tweet())
            self.assertEqual(outcome.status, TweetStatus.FILTERED)
            self.assertIn("广告", store.get("1234567890").reason)
            store.close()

    async def test_llm_failure_defers(self):
        from bxbot.media import MediaDownloader
        from bxbot.pipeline import build_filter_chain

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cfg = self._cfg(tmp_path)
            store = StateStore(cfg.db_path)
            translator = StubTranslator(fail=True)
            pipeline = Pipeline(
                cfg,
                store,
                build_filter_chain(cfg, translator),
                translator,
                MediaDownloader(cfg.tmp_dir),
                PublishDispatcher(DryRunPublisher()),
            )
            outcome = await pipeline.process(make_tweet())
            self.assertEqual(outcome.status, TweetStatus.PENDING)
            row = store.get("1234567890")
            self.assertEqual(row.status, "pending")
            self.assertEqual(row.attempt_count, 0)  # 不消耗次数
            store.close()

    async def test_video_dispatch(self):
        from bxbot.media import MediaDownloader
        from bxbot.pipeline import build_filter_chain

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cfg = self._cfg(tmp_path)
            store = StateStore(cfg.db_path)
            translator = StubTranslator()
            tweet = make_tweet(
                media=[
                    MediaAsset(
                        kind=MediaKind.PHOTO,
                        url="https://pbs.twimg.com/media/x?name=large",
                    ),
                    MediaAsset(
                        kind=MediaKind.VIDEO, url="https://video.twimg.com/x.m3u8"
                    ),
                ]
            )
            self.assertEqual(tweet.media_kind, MediaKind.MIXED)
            pipeline = Pipeline(
                cfg,
                store,
                build_filter_chain(cfg, translator),
                translator,
                MediaDownloader(cfg.tmp_dir),
                PublishDispatcher(DryRunPublisher()),
            )
            # MIXED 只有 m3u8（无 mp4 直链）→ 下载阶段报错 → failed（不外抛、不联网）
            outcome = await pipeline.process(tweet)
            self.assertEqual(outcome.status, TweetStatus.FAILED)
            store.close()


if __name__ == "__main__":
    unittest.main()
