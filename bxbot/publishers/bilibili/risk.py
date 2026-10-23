"""B 站风控错误识别：风控类错误转 BiliRiskError（熔断），其余照常抛出。"""

from __future__ import annotations

from functools import wraps

from loguru import logger

from bxbot.pipeline import BiliRiskError

# 常见风控/拦截错误码（owner-bili-apis/errcode + 抓包经验）：
# -352 风控校验失败、-403 风控拦截/权限不足、-412 请求被拦截（IP 风控）、
# -799 请求过于频繁、-304 投稿过快、21070 投稿频繁
RISK_CODES = {-352, -403, -412, -304, -799, 21070, 21069, 4121036}
RISK_KEYWORDS = ("风控", "频繁", "拦截", "拒绝访问", "访问权限", "captcha", "challenge")


def is_risk_error(exc: Exception) -> bool:
    code = getattr(exc, "code", None)
    if code in RISK_CODES:
        return True
    msg = str(exc).lower()
    return any(k.lower() in msg for k in RISK_KEYWORDS)


def wrap_bili_errors(fn):
    """装饰发布方法：风控错误 → BiliRiskError；其他异常原样抛（pipeline 计入重试）。"""

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except BiliRiskError:
            raise
        except Exception as e:
            if is_risk_error(e):
                logger.error(f"B 站风控错误：{e}")
                raise BiliRiskError(str(e)) from e
            raise

    return wrapper
