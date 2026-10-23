"""Windows 兼容小工具：信号处理、路径。"""

from __future__ import annotations

import asyncio
import signal


def install_stop_signals(
    loop: asyncio.AbstractEventLoop, stop_event: asyncio.Event
) -> None:
    """把 Ctrl+C / SIGTERM / SIGBREAK 映射到 stop_event（Windows 不支持 add_signal_handler）。"""

    def _handler(signum, _frame):
        loop.call_soon_threadsafe(stop_event.set)

    for name in ("SIGINT", "SIGTERM", "SIGBREAK"):
        sig = getattr(signal, name, None)
        if sig is None:
            continue
        try:
            signal.signal(sig, _handler)
        except (ValueError, OSError):
            pass
