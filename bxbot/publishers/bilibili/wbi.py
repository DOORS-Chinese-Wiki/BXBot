"""WBI 签名（按 owner-bili-apis/auth/sign/wbi.md 实现）。

算法：
1. GET /x/web-interface/nav 取 wbi_img.img_url / sub_url，文件名即 img_key / sub_key（每日更替，缓存）
2. raw = img_key + sub_key，按 MIXIN_KEY_ENC_TAB 重排取前 32 位 → mixin_key
3. 参数加 wts（秒级时间戳）→ 按键名升序 → 过滤 !'()* → URL 编码（字母大写、空格 %20）
4. w_rid = md5(query + mixin_key)
"""

from __future__ import annotations

import hashlib
import time
import urllib.parse
from functools import reduce

import httpx
from loguru import logger

MIXIN_KEY_ENC_TAB = [
    46,
    47,
    18,
    2,
    53,
    8,
    23,
    32,
    15,
    50,
    10,
    31,
    58,
    3,
    45,
    35,
    27,
    43,
    5,
    49,
    33,
    9,
    42,
    19,
    29,
    28,
    14,
    39,
    12,
    38,
    41,
    13,
    37,
    48,
    7,
    16,
    24,
    55,
    40,
    61,
    26,
    17,
    0,
    1,
    60,
    51,
    30,
    4,
    22,
    25,
    54,
    21,
    56,
    59,
    6,
    63,
    57,
    62,
    11,
    36,
    20,
    34,
    44,
    52,
]

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

_FILTER_CHARS = "!'()*"


def get_mixin_key(raw_wbi_key: str) -> str:
    return reduce(lambda s, i: s + raw_wbi_key[i], MIXIN_KEY_ENC_TAB, "")[:32]


def sign_params(
    params: dict, img_key: str, sub_key: str, wts: int | None = None
) -> dict:
    """给请求参数做 WBI 签名，返回带 w_rid/wts 的新 dict（不修改入参）。

    按文档参考实现：值中过滤 !'()* 后的结果即最终请求参数。
    """
    mixin_key = get_mixin_key(img_key + sub_key)
    signed = dict(params)
    signed["wts"] = int(wts if wts is not None else round(time.time()))
    signed = dict(sorted(signed.items()))
    # 过滤 !'()*，URL 编码（quote 保证空格→%20、字母大写）
    filtered = {
        k: "".join(c for c in str(v) if c not in _FILTER_CHARS)
        for k, v in signed.items()
    }
    query = urllib.parse.urlencode(filtered, quote_via=urllib.parse.quote)
    filtered["w_rid"] = hashlib.md5((query + mixin_key).encode()).hexdigest()
    return filtered


class WbiSigner:
    """管理 img_key/sub_key 的获取与缓存（每日更替，失败可强制刷新）。"""

    def __init__(self, client: httpx.AsyncClient):
        self._client = client
        self._img_key: str = ""
        self._sub_key: str = ""
        self._fetched_at: float = 0.0

    async def refresh(self) -> None:
        # B 站对无浏览器 UA 的请求直接 412 风控，这里强制带 UA/Referer
        resp = await self._client.get(
            "https://api.bilibili.com/x/web-interface/nav",
            headers={"User-Agent": _UA, "Referer": "https://www.bilibili.com/"},
        )
        resp.raise_for_status()
        data = resp.json().get("data") or {}
        wbi_img = data.get("wbi_img") or {}
        img_url = wbi_img.get("img_url") or ""
        sub_url = wbi_img.get("sub_url") or ""
        if not img_url or not sub_url:
            raise RuntimeError(f"nav 接口未返回 wbi_img：{resp.text[:120]}")
        self._img_key = img_url.rsplit("/", 1)[1].split(".")[0]
        self._sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
        self._fetched_at = time.time()
        logger.debug(
            f"WBI keys 已刷新：img={self._img_key[:8]}… sub={self._sub_key[:8]}…"
        )

    async def sign(self, params: dict, wts: int | None = None) -> dict:
        if not self._img_key or time.time() - self._fetched_at > 6 * 3600:
            await self.refresh()
        return sign_params(params, self._img_key, self._sub_key, wts=wts)

    def invalidate(self) -> None:
        self._img_key = ""
        self._sub_key = ""
