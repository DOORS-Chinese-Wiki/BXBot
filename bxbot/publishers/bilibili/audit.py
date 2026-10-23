"""视频稿件审核状态查询（按 owner-bili-apis/bili-video-audit-api.md）。

GET https://member.bilibili.com/x/web/detail/audit?bvid=...
state: -4=审核驳回  0=审核中  1=审核通过
"""

from __future__ import annotations

import httpx
from loguru import logger

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

STATE_TEXT = {-4: "审核驳回", 0: "审核中", 1: "审核通过"}


async def get_audit_status(bvid: str, cookies: dict[str, str], proxy: str = "") -> dict:
    """查询审核状态，返回 {state, state_text, reject_reason}。"""
    cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items() if v)
    async with httpx.AsyncClient(proxy=proxy or None, timeout=20) as client:
        resp = await client.get(
            "https://member.bilibili.com/x/web/detail/audit",
            params={"bvid": bvid, "web_location": "0.0"},
            headers={
                "User-Agent": _UA,
                "Referer": "https://member.bilibili.com/",
                "Cookie": cookie_header,
            },
        )
        payload = resp.json()
    if payload.get("code") != 0:
        logger.warning(
            f"审核状态查询失败：{payload.get('code')} {payload.get('message')}"
        )
        return {
            "state": None,
            "state_text": "查询失败",
            "reject_reason": str(payload.get("message", "")),
        }
    data = payload.get("data") or {}
    state = data.get("state")
    reject = ""
    for p in data.get("problem_detail") or []:
        if p.get("reject_reason"):
            reject = p["reject_reason"]
            break
    result = {
        "state": state,
        "state_text": STATE_TEXT.get(state, f"状态{state}"),
        "reject_reason": reject,
    }
    logger.info(
        f"稿件 {bvid} 审核状态：{result['state_text']}"
        + (f"（{reject[:50]}…）" if reject else "")
    )
    return result
