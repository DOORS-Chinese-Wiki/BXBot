"""OpenAI 兼容 /chat/completions 翻译 + 同步判断（单次调用产出 JSON）。"""

from __future__ import annotations

import asyncio
import json
import re
import time
from pathlib import Path

import httpx
from loguru import logger

from bxbot.config import LLMConfig
from bxbot.models import LLMResult, MediaKind, NormalizedTweet
from bxbot.translate.base import TranslateError

DEFAULT_SYSTEM_PROMPT = """你是推文本地化与内容审核助手。把用户给出的推文翻译成简体中文，并判断是否适合同步发布到 B 站动态/视频稿件。只输出一个 JSON 对象，不要任何任何其他文字：
{
  "translate": "简体中文译文，保留语气与 emoji",
  "should_sync": true或false,
  "reason": "若 should_sync 为 false，用一句中文说明原因；否则留空字符串",
  "title_zh": "适合 B 站视频稿件的标题，不超过40字；没有合适标题时给译文摘要",
  "tags": ["最多5个中文标签，不要带#号"]
}
判定 should_sync=false 的情形：广告/营销推广、抽奖/求转发求关注、NSFW/色情低俗、政治敏感或涉政谣言、辱骂仇恨、纯互动内容（投票/问答/早安晚安）、重复刷屏、明显不适合 B 站社区氛围的内容。
纯中文推文：translate 给出原文（可轻度润色），其余照常判断。"""

_FENCE_PAT = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def _parse_llm_json(content: str) -> dict:
    """容错解析：剥 ```json 围栏，截取首个 {...}。"""
    text = _FENCE_PAT.sub("", content.strip()).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


class OpenAICompatTranslator:
    def __init__(self, cfg: LLMConfig, proxy: str = "", prompt_override: str = ""):
        self._cfg = cfg
        self._system_prompt = prompt_override or DEFAULT_SYSTEM_PROMPT
        self._client = httpx.AsyncClient(
            base_url=cfg.base_url.rstrip("/"),
            timeout=httpx.Timeout(cfg.timeout_s),
            proxy=proxy or None,
            headers={"Authorization": f"Bearer {cfg.api_key}"} if cfg.api_key else {},
        )
        self._json_mode_failed = (
            False  # json_mode=auto 下记录 response_format 是否被拒绝
        )
        self._consec_fails = 0  # 连续失败计数（全局熔断）
        self._breaker_until = 0.0  # 熔断截止时间（monotonic）

    async def close(self) -> None:
        await self._client.aclose()

    @classmethod
    def from_config(cls, cfg: LLMConfig, proxy: str = "") -> OpenAICompatTranslator:
        prompt = ""
        if cfg.prompt_file and Path(cfg.prompt_file).exists():
            prompt = Path(cfg.prompt_file).read_text(encoding="utf-8")
        return cls(cfg, proxy=proxy, prompt_override=prompt)

    # ---- 主入口 ----

    async def translate_and_judge(self, tweet: NormalizedTweet) -> LLMResult:
        if time.monotonic() < self._breaker_until:
            raise TranslateError("LLM 连续失败，全局熔断冷却中")

        payload = {
            "text": tweet.text,
            "lang": tweet.lang or "unknown",
            "has_video": tweet.media_kind
            in (MediaKind.VIDEO, MediaKind.GIF, MediaKind.MIXED),
            "has_photos": tweet.media_kind in (MediaKind.PHOTO, MediaKind.MIXED),
            "is_retweet": tweet.is_retweet,
            "is_reply": tweet.is_reply,
        }
        try:
            content = await self._chat_json(payload, temperature=self._cfg.temperature)
            try:
                data = _parse_llm_json(content)
            except (json.JSONDecodeError, ValueError):
                logger.warning("LLM 返回 JSON 解析失败，用 temperature=0 重试一次")
                content = await self._chat_json(payload, temperature=0.0)
                try:
                    data = _parse_llm_json(content)
                except (json.JSONDecodeError, ValueError) as e:
                    raise TranslateError(
                        f"LLM 返回无法解析为 JSON：{content[:200]}"
                    ) from e
        except TranslateError:
            self._record_fail()
            raise
        self._consec_fails = 0

        should_sync = data.get("should_sync", True)
        if isinstance(should_sync, str):
            should_sync = should_sync.strip().lower() not in ("false", "no", "0")
        tags = data.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        return LLMResult(
            translate_zh=str(data.get("translate") or tweet.text),
            should_sync=bool(should_sync),
            reason=str(data.get("reason") or ""),
            title_zh=(str(data["title_zh"]) if data.get("title_zh") else None),
            tags=[str(t) for t in tags][:5],
        )

    def _record_fail(self) -> None:
        self._consec_fails += 1
        if self._consec_fails >= 5:
            self._breaker_until = time.monotonic() + 300
            self._consec_fails = 0
            logger.warning("LLM 连续失败 5 次，全局熔断 300s")

    async def healthcheck(self) -> bool:
        try:
            resp = await self._client.get("/models")
            return resp.status_code == 200
        except Exception:
            return False

    # ---- HTTP ----

    async def _chat_json(self, payload: dict, temperature: float) -> str:
        body: dict = {
            "model": self._cfg.model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
        }
        use_json_mode = self._cfg.json_mode == "on" or (
            self._cfg.json_mode == "auto" and not self._json_mode_failed
        )
        if use_json_mode:
            body["response_format"] = {"type": "json_object"}

        last_err: Exception | None = None
        for attempt in range(1, self._cfg.max_retries + 1):
            try:
                resp = await self._client.post("/chat/completions", json=body)
            except httpx.HTTPError as e:
                last_err = e
                await asyncio.sleep(min(2**attempt, 16))
                continue

            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", 5))
                logger.warning(
                    f"LLM 429 限流，等待 {retry_after:.0f}s（{tweet_short(payload)}）"
                )
                await asyncio.sleep(min(retry_after, 120))
                last_err = TranslateError("429 rate limited")
                continue
            if (
                resp.status_code == 400
                and use_json_mode
                and self._cfg.json_mode == "auto"
            ):
                # 部分国产/Ollama 模型不支持 response_format，去掉后重试
                self._json_mode_failed = True
                body.pop("response_format", None)
                use_json_mode = False
                logger.info("LLM 不支持 response_format，已降级为纯文本模式")
                continue
            if resp.status_code >= 500:
                last_err = TranslateError(f"LLM 服务错误 {resp.status_code}")
                await asyncio.sleep(min(2**attempt, 16))
                continue
            if resp.status_code != 200:
                raise TranslateError(
                    f"LLM 请求失败 {resp.status_code}: {resp.text[:200]}"
                )

            data = resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError) as e:
                raise TranslateError(f"LLM 响应结构异常：{str(data)[:200]}") from e

        raise TranslateError(f"LLM 调用重试耗尽：{last_err}")


def tweet_short(payload: dict) -> str:
    text = str(payload.get("text", ""))
    return text[:20] + ("…" if len(text) > 20 else "")
