"""SQLite 状态存储：tweet_id 去重 + 处理状态机 + 水位。"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from bxbot.models import TweetStatus

_SCHEMA = """
CREATE TABLE IF NOT EXISTS tweets (
  tweet_id      TEXT PRIMARY KEY,
  status        TEXT NOT NULL,
  media_kind    TEXT,
  reason        TEXT,
  attempt_count INTEGER DEFAULT 0,
  last_error    TEXT,
  result_json   TEXT,
  created_at    TEXT,
  updated_at    TEXT
);
CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT
);
"""


@dataclass
class TweetRow:
    tweet_id: str
    status: str
    media_kind: str | None
    reason: str | None
    attempt_count: int
    last_error: str | None
    result_json: str | None
    created_at: str | None
    updated_at: str | None


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class StateStore:
    """线程不安全的轻量封装；asyncio 单线程内使用，写操作由调用方串行化。"""

    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # ---- 去重与状态 ----

    def try_begin(self, tweet_id: str) -> bool:
        """首次发现返回 True（已插入 pending）；已存在返回 False。"""
        cur = self._conn.execute(
            "INSERT OR IGNORE INTO tweets (tweet_id, status, attempt_count, created_at, updated_at)"
            " VALUES (?, ?, 0, ?, ?)",
            (tweet_id, TweetStatus.PENDING.value, _now(), _now()),
        )
        self._conn.commit()
        return cur.rowcount == 1

    def get(self, tweet_id: str) -> TweetRow | None:
        row = self._conn.execute(
            "SELECT * FROM tweets WHERE tweet_id = ?", (tweet_id,)
        ).fetchone()
        return self._to_row(row) if row else None

    def mark(
        self,
        tweet_id: str,
        status: TweetStatus,
        *,
        reason: str | None = None,
        error: str | None = None,
        result_json: str | None = None,
        media_kind: str | None = None,
        inc_attempt: bool = False,
    ) -> None:
        sets = ["status = ?", "updated_at = ?"]
        args: list[object] = [status.value, _now()]
        if reason is not None:
            sets.append("reason = ?")
            args.append(reason)
        if error is not None:
            sets.append("last_error = ?")
            args.append(error)
        if result_json is not None:
            sets.append("result_json = ?")
            args.append(result_json)
        if media_kind is not None:
            sets.append("media_kind = ?")
            args.append(media_kind)
        if inc_attempt:
            sets.append("attempt_count = attempt_count + 1")
        args.append(tweet_id)
        self._conn.execute(
            f"UPDATE tweets SET {', '.join(sets)} WHERE tweet_id = ?", args
        )
        self._conn.commit()

    def retryable_failed(self, max_attempts: int) -> list[TweetRow]:
        """启动/每轮捞出可重试的 failed 行。"""
        rows = self._conn.execute(
            "SELECT * FROM tweets WHERE status = ? AND attempt_count < ?",
            (TweetStatus.FAILED.value, max_attempts),
        ).fetchall()
        return [self._to_row(r) for r in rows]

    def pending_rows(self) -> list[TweetRow]:
        """捞出 pending 行（LLM 故障推迟、崩溃中断的处理）。"""
        rows = self._conn.execute(
            "SELECT * FROM tweets WHERE status = ?", (TweetStatus.PENDING.value,)
        ).fetchall()
        return [self._to_row(r) for r in rows]

    def counts(self) -> dict[str, int]:
        rows = self._conn.execute(
            "SELECT status, COUNT(*) AS n FROM tweets GROUP BY status"
        ).fetchall()
        return {r["status"]: r["n"] for r in rows}

    # ---- 水位 / meta ----

    def get_meta(self, key: str) -> str | None:
        row = self._conn.execute(
            "SELECT value FROM meta WHERE key = ?", (key,)
        ).fetchone()
        return row["value"] if row else None

    def set_meta(self, key: str, value: str) -> None:
        self._conn.execute(
            "INSERT INTO meta (key, value) VALUES (?, ?)"
            " ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        self._conn.commit()

    @staticmethod
    def _to_row(row: sqlite3.Row) -> TweetRow:
        return TweetRow(
            tweet_id=row["tweet_id"],
            status=row["status"],
            media_kind=row["media_kind"],
            reason=row["reason"],
            attempt_count=row["attempt_count"],
            last_error=row["last_error"],
            result_json=row["result_json"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
