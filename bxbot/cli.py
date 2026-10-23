"""命令行入口：init / login-bili / login-x / doctor / once / run。"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
import sys
from pathlib import Path

from loguru import logger

from bxbot import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bxbot",
        description="BXBot —— 推特自动同步到 B 站机器人",
    )
    parser.add_argument("--version", action="version", version=f"bxbot {__version__}")
    parser.add_argument(
        "--config", default=None, help="配置文件路径（默认 ./config.yaml）"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="生成 config.yaml/.env/data 目录骨架")
    sub.add_parser("login-bili", help="B 站扫码登录（凭证存入 data/cookies/）")

    p_login_x = sub.add_parser("login-x", help="导入 X/Twitter cookies")
    p_login_x.add_argument(
        "--cookie", help="cookie 字符串，如 'auth_token=xxx; ct0=yyy'"
    )
    p_login_x.add_argument("--file", help="cookies JSON 文件路径（键值对格式）")

    sub.add_parser("doctor", help="环境与凭证自检")

    p_once = sub.add_parser("once", help="执行一轮同步（拉取→过滤→翻译→发布）")
    p_once.add_argument("--tweet-id", help="只处理指定推文（调试回放）")
    p_once.add_argument(
        "--force", action="store_true", help="跳过内容过滤强制同步（人工指定）"
    )
    p_once.add_argument("--dry-run", action="store_true", help="不真发 B 站，只打印")

    p_run = sub.add_parser("run", help="常驻轮询")
    p_run.add_argument("--dry-run", action="store_true", help="不真发 B 站，只打印")
    return parser


def main(argv: list[str] | None = None) -> int:
    # Windows 控制台默认 GBK，统一 UTF-8 输出避免中文乱码
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    if args.command == "init":
        return cmd_init(args)
    return _run_async(args)


def _run_async(args: argparse.Namespace) -> int:
    try:
        return asyncio.run(_async_main(args))
    except KeyboardInterrupt:
        logger.info("已中断")
        return 130


async def _async_main(args: argparse.Namespace) -> int:
    from bxbot.config import ConfigError, ensure_runtime_dirs, load_config
    from bxbot.utils.logging import setup_logging

    try:
        cfg = load_config(args.config)
    except ConfigError as e:
        print(f"配置错误：{e}")
        return 2
    ensure_runtime_dirs(cfg)
    setup_logging(cfg.logs_dir)

    if args.command == "login-bili":
        return await cmd_login_bili(cfg)
    if args.command == "login-x":
        return await cmd_login_x(cfg, args)
    if args.command == "doctor":
        return await cmd_doctor(cfg)
    if args.command == "once":
        return await cmd_once(cfg, args)
    if args.command == "run":
        return await cmd_run(cfg, args)
    return 1


# ---- init（同步，不需要配置） ----


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.config).resolve().parent if args.config else Path.cwd()
    created = []
    for src, dst in (("config.example.yaml", "config.yaml"), (".env.example", ".env")):
        s, d = root / src, root / dst
        if d.exists():
            print(f"跳过（已存在）：{d}")
        elif not s.exists():
            print(f"缺少模板：{s}")
        else:
            shutil.copyfile(s, d)
            created.append(d)
            print(f"已生成：{d}")
    for d in ("data", "data/cookies", "data/tmp", "data/logs"):
        (root / d).mkdir(parents=True, exist_ok=True)
    print(f"\n数据目录就绪：{root / 'data'}")
    if created:
        print(
            "请编辑 config.yaml（目标账号）与 .env（LLM_API_KEY），然后运行 python -m bxbot doctor"
        )
    return 0


# ---- login-bili ----


async def cmd_login_bili(cfg) -> int:
    from bxbot.publishers.bilibili import auth

    print("正在生成登录二维码…")
    cred = await auth.login_qrcode()
    auth.save_cred(cred, cfg.bili_cred_path)
    print(f"登录成功，凭证已保存到 {cfg.bili_cred_path}")
    return 0


# ---- login-x ----


async def cmd_login_x(cfg, args) -> int:
    cookies: dict[str, str] = {}

    if args.file:
        raw = json.loads(Path(args.file).read_text(encoding="utf-8"))
        cookies = {str(k): str(v) for k, v in raw.items()}
    elif args.cookie:
        cookies = _parse_cookie_string(args.cookie)
    else:
        print(
            "请粘贴浏览器里的 X/Twitter cookies（形如 'auth_token=xxx; ct0=yyy'），回车结束："
        )
        try:
            line = sys.stdin.readline().strip()
        except (EOFError, KeyboardInterrupt):
            line = ""
        cookies = _parse_cookie_string(line)

    if not cookies:
        print("未解析到任何 cookie")
        return 1
    if "auth_token" not in cookies or "ct0" not in cookies:
        print(
            f"警告：缺少 auth_token 或 ct0（当前 keys: {sorted(cookies.keys())}），twikit 登录可能失败"
        )

    cfg.x_cookies_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.x_cookies_path.write_text(
        json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"X cookies 已保存到 {cfg.x_cookies_path}（含 {len(cookies)} 个字段）")
    return 0


def _parse_cookie_string(s: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in re.split(r";\s*", s.strip()):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


# ---- doctor ----


async def cmd_doctor(cfg) -> int:

    print(f"── BXBot doctor（config: {cfg.target.handle}）──")
    ok = True

    # 1) 配置
    print(
        f"[{'OK' if cfg.target.handle else 'FAIL'}] 配置加载正常（数据目录 {cfg.data_dir}）"
    )

    # 2) LLM
    key = cfg.llm.api_key
    masked = (key[:4] + "****") if key else "(空)"
    print(f"[INFO] LLM: {cfg.llm.model} @ {cfg.llm.base_url} key={masked}")
    if (
        not key
        and "localhost" not in cfg.llm.base_url
        and "127.0.0.1" not in cfg.llm.base_url
    ):
        print("[WARN] LLM_API_KEY 为空（本地 Ollama 可忽略）")
    from bxbot.translate.openai_compat import OpenAICompatTranslator

    translator = OpenAICompatTranslator.from_config(cfg.llm)
    healthy = await translator.healthcheck()
    await translator.close()
    print(
        f"[{'OK' if healthy else 'WARN'}] LLM 连通性：{'正常' if healthy else '不可达（检查 base_url/网络/key）'}"
    )

    # 3) B 站凭证
    from bxbot.publishers.bilibili import auth as bili_auth

    cred = bili_auth.load_cred(cfg.bili_cred_path)
    if cred and cred.sessdata:
        try:
            info = await bili_auth.probe(cred)
            print(
                f"[OK] B 站登录有效：{info.get('uname', '?')} (uid={info.get('mid', '?')})"
            )
        except Exception as e:
            ok = False
            print(f"[FAIL] B 站凭证失效（{e}），运行 python -m bxbot login-bili")
    else:
        print("[WARN] 尚未登录 B 站，运行 python -m bxbot login-bili")

    # 4) X cookies
    if cfg.x_cookies_path.exists():
        cookies = json.loads(cfg.x_cookies_path.read_text(encoding="utf-8"))
        print(
            f"[OK] X cookies 存在（{len(cookies)} 字段，auth_token={'有' if 'auth_token' in cookies else '无'}）"
        )
    else:
        print("[INFO] X cookies 不存在（twikit 将尝试 guest 模式；失败则运行 login-x）")

    # 5) 状态库
    from bxbot.state import StateStore

    store = StateStore(cfg.db_path)
    counts = store.counts()
    watermark = store.get_meta("watermark_id")
    store.close()
    print(
        f"[OK] 状态库 {cfg.db_path.name}：{counts or '空'} 水位={watermark or '未建立'}"
    )

    # 6) ffmpeg（可选）
    has_ffmpeg = shutil.which("ffmpeg") is not None
    print(
        f"[{'OK' if has_ffmpeg else 'INFO'}] ffmpeg：{'可用' if has_ffmpeg else '未安装（封面用缩略图/占位图，可选）'}"
    )

    print(f"\n结论：{'一切就绪' if ok else '存在需要修复的问题'}")
    return 0 if ok else 1


# ---- once / run ----


async def cmd_once(cfg, args) -> int:
    from bxbot.fetchers import FetchError
    from bxbot.publishers.bilibili.publisher import BiliCredentialsMissing
    from bxbot.scheduler import run_once

    try:
        stats = await run_once(
            cfg, dry_run=args.dry_run, tweet_id=args.tweet_id, force=args.force
        )
    except (FetchError, BiliCredentialsMissing) as e:
        print(f"执行失败：{e}")
        print(
            "提示：login-bili / login-x 完成登录，或在 config.yaml 配置 twitter.proxy；调试可加 --dry-run"
        )
        return 1
    print(
        f"本轮完成：拉取 {stats.fetched} 发布 {stats.published} "
        f"过滤 {stats.filtered} 失败 {stats.failed} 推迟 {stats.deferred}"
    )
    for note in stats.notes:
        print(f"  · {note}")
    return 0


async def cmd_run(cfg, args) -> int:
    from bxbot.scheduler import run_forever

    await run_forever(cfg, dry_run=args.dry_run)
    return 0
