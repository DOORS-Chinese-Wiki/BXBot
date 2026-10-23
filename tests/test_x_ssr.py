"""x_ssr 页面解析测试（用服务器实抓的 DoorsWiki 页面作样本）。"""

from __future__ import annotations

import unittest
from datetime import UTC
from pathlib import Path

from bxbot.fetchers.x_ssr import extract_tweets_from_html

FIXTURE = Path(__file__).parent / "fixtures" / "doorswiki.html"


class TestXSsrExtract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = FIXTURE.read_text(encoding="utf-8", errors="replace")
        cls.tweets = extract_tweets_from_html(cls.html, fallback_handle="DoorsWiki")

    def test_extracts_tweets(self):
        self.assertGreaterEqual(len(self.tweets), 4)

    def test_ids_unique_and_numeric(self):
        ids = [t.tweet_id for t in self.tweets]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertTrue(i.isdigit(), i)

    def test_text_content(self):
        texts = "\n".join(t.text for t in self.tweets)
        self.assertIn("tier list", texts)
        self.assertIn("wiki", texts.lower())

    def test_author(self):
        # 至少大部分推文作者应是 DoorsWiki（引用/转推里可能是别人）
        handles = [t.author_handle for t in self.tweets]
        self.assertGreaterEqual(handles.count("DoorsWiki"), 1)

    def test_timestamps_parsed(self):
        from datetime import datetime

        for t in self.tweets:
            self.assertIsInstance(t.created_at, datetime)
            self.assertEqual(t.created_at.tzinfo, UTC)
            self.assertGreater(t.created_at.year, 2020)

    def test_photos_extracted(self):
        photo_tweets = [t for t in self.tweets if t.media]
        self.assertGreaterEqual(len(photo_tweets), 1)
        for t in photo_tweets:
            for m in t.media:
                if m.kind.value == "photo":
                    self.assertIn("pbs.twimg.com/media/", m.url)
                    self.assertIn("name=orig", m.url)

    def test_sorted_ascending(self):
        ids = [int(t.tweet_id) for t in self.tweets]
        self.assertEqual(ids, sorted(ids))

    def test_url_built(self):
        for t in self.tweets:
            self.assertIn(f"/status/{t.tweet_id}", t.url)


if __name__ == "__main__":
    unittest.main()
