"""重试策略工厂：指数退避 + 抖动。"""

from __future__ import annotations

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)


def async_retry(max_attempts: int = 3, base: float = 1.0, cap: float = 16.0):
    """通用异步重试装饰器（网络类异常重试，耗尽后 reraise）。"""
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential_jitter(initial=base, max=cap),
        retry=retry_if_exception_type((Exception,)),
    )
