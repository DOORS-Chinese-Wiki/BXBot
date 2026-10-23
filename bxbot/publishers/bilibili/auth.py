"""B 站登录与凭证管理：扫码登录、cookie 持久化、鉴权探测。"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from bilibili_api import Credential


def save_cred(cred, path: Path) -> None:
    """Credential → JSON 落盘（永不进 git）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "SESSDATA": cred.sessdata or "",
        "bili_jct": cred.bili_jct or "",
        "buvid3": getattr(cred, "buvid3", "") or "",
        "buvid4": getattr(cred, "buvid4", "") or "",
        "DedeUserID": getattr(cred, "dedeuserid", "") or "",
        "ac_time_value": getattr(cred, "ac_time_value", "") or "",
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"B 站凭证已保存：{path}")


def load_cred(path: Path):
    """读取凭证文件，返回 Credential 或 None。"""
    from bilibili_api import Credential

    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return Credential(
        sessdata=data.get("SESSDATA") or None,
        bili_jct=data.get("bili_jct") or None,
        buvid3=data.get("buvid3") or None,
        buvid4=data.get("buvid4") or None,
        dedeuserid=data.get("DedeUserID") or None,
        ac_time_value=data.get("ac_time_value") or None,
    )


async def login_qrcode() -> Credential:
    """终端扫码登录（raw passport 接口，绕开归档库的 cookie 解析 bug）。

    归档库 login_v2 从 data.url 解析 cookie 在新版返回格式下会拿到空 SESSDATA，
    这里直接对接 passport qrcode/generate + poll，兼容 cookie_info 与 url 查询串两种形态。
    """
    import urllib.parse

    import httpx
    from bilibili_api import Credential

    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    async with httpx.AsyncClient(timeout=20, headers={"User-Agent": ua}) as client:
        gen = (
            await client.get(
                "https://passport.bilibili.com/x/passport-login/web/qrcode/generate",
                params={"source": "main-fe-header"},
            )
        ).json()
        if gen.get("code") != 0:
            raise RuntimeError(f"获取登录二维码失败：{gen}")
        qr_url = gen["data"]["url"]
        qr_key = gen["data"]["qrcode_key"]

        try:
            import qrcode

            qr = qrcode.QRCode()
            qr.add_data(qr_url)
            qr.make(fit=True)
            print("\n请使用哔哩哔哩手机客户端扫描下方二维码登录：\n")
            qr.print_ascii(invert=True)
        except Exception:
            print(f"\n请扫描二维码（内容）：\n{qr_url}\n")

        for _ in range(60):  # 3 分钟
            resp = (
                await client.get(
                    "https://passport.bilibili.com/x/passport-login/web/qrcode/poll",
                    params={"qrcode_key": qr_key, "source": "main-fe-header"},
                )
            ).json()
            data = resp.get("data") or {}
            code = data.get("code")
            if code == 0:
                cookies: dict[str, str] = {}
                for item in (data.get("cookie_info") or {}).get("cookies") or []:
                    if item.get("name") and item.get("value"):
                        cookies[item["name"]] = item["value"]
                if "?" in (data.get("url") or ""):
                    for k, v in urllib.parse.parse_qsl(data["url"].split("?", 1)[1]):
                        if k and v:
                            cookies.setdefault(k, v)
                if not cookies.get("SESSDATA") or not cookies.get("bili_jct"):
                    raise RuntimeError(f"登录成功但 cookie 解析失败：{str(data)[:200]}")
                cred = Credential(
                    sessdata=cookies.get("SESSDATA"),
                    bili_jct=cookies.get("bili_jct"),
                    buvid3=cookies.get("buvid3"),
                    buvid4=cookies.get("buvid4"),
                    dedeuserid=cookies.get("DedeUserID"),
                    ac_time_value=data.get("refresh_token"),
                )
                logger.info("B 站扫码登录成功")
                return cred
            if code == 86038:
                raise RuntimeError("二维码已过期，请重新运行 login-bili")
            if code == 86090:
                print("已扫描，请在手机上确认…", end="\r")
            else:
                print("等待扫描…", end="\r")
            await asyncio.sleep(3)
        raise RuntimeError("等待登录超时（3 分钟）")


async def probe(cred) -> dict:
    """轻量鉴权探测：能取到自身信息即凭证有效。"""
    from bilibili_api import user

    return await user.get_self_info(credential=cred)


def cred_to_cookies(cred) -> dict[str, str]:
    """Credential → 原始 cookie dict（供自研 HTTP 层使用）。"""
    return {
        "SESSDATA": cred.sessdata or "",
        "bili_jct": cred.bili_jct or "",
        "buvid3": getattr(cred, "buvid3", "") or "",
        "buvid4": getattr(cred, "buvid4", "") or "",
        "DedeUserID": getattr(cred, "dedeuserid", "") or "",
    }
