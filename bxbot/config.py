"""配置加载：config.yaml（${ENV_VAR} 展开）+ .env，pydantic 校验。"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Literal

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

_ENV_PAT = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


class TargetConfig(BaseModel):
    handle: str


class TwitterConfig(BaseModel):
    backend_order: list[str] = ["twikit", "fxtwitter"]
    proxy: str = ""
    page_size: int = 20


class LLMConfig(BaseModel):
    base_url: str = "https://api.deepseek.com/v1"
    api_key: str = ""
    model: str = "deepseek-chat"
    temperature: float = 0.2
    timeout_s: float = 60.0
    max_retries: int = 3
    json_mode: Literal["auto", "on", "off"] = "auto"
    on_failure: Literal["skip", "post_original"] = "skip"
    prompt_file: str = ""


class FilterConfig(BaseModel):
    skip_retweets: bool = False
    skip_replies: bool = False
    skip_quotes: bool = False
    keyword_blacklist: list[str] = Field(default_factory=list)
    llm_enabled: bool = True
    max_images: int = 9
    max_video_mb: int = 512
    max_video_s: int = 1800


class TranslateConfig(BaseModel):
    mode: Literal["both", "translated_only", "original_only"] = "both"
    always_include_source_link: bool = True


class BiliConfig(BaseModel):
    dry_run: bool = False
    proxy: str = ""
    tid: int = 21
    tags: list[str] = Field(default_factory=lambda: ["推特搬运", "资讯"])
    copyright: int = 2
    desc_max_len: int = 2000
    publish_gap_seconds: int = 60
    max_publish_per_round: int = 5
    risk_cooldown_s: int = 1800
    aigc_flag: int = 0  # 动态 option.aigc：0=非AI 1=AI生成 2=AI辅助
    risk_params: dict[str, str] = Field(
        default_factory=dict
    )  # b_wet / dm_* 等风控参数透传


class PollConfig(BaseModel):
    interval_seconds: int = 600
    max_attempts: int = 3


class PathsConfig(BaseModel):
    data_dir: str = "data"


class Config(BaseModel):
    target: TargetConfig
    twitter: TwitterConfig = Field(default_factory=TwitterConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    filter: FilterConfig = Field(default_factory=FilterConfig)
    translate: TranslateConfig = Field(default_factory=TranslateConfig)
    bilibili: BiliConfig = Field(default_factory=BiliConfig)
    poll: PollConfig = Field(default_factory=PollConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)

    # ---- 运行时派生路径（不进 YAML）----
    project_root: Path = Path(".")

    @property
    def data_dir(self) -> Path:
        return (self.project_root / self.paths.data_dir).resolve()

    @property
    def cookies_dir(self) -> Path:
        return self.data_dir / "cookies"

    @property
    def tmp_dir(self) -> Path:
        return self.data_dir / "tmp"

    @property
    def logs_dir(self) -> Path:
        return self.data_dir / "logs"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "state.db"

    @property
    def bili_cred_path(self) -> Path:
        return self.cookies_dir / "bili_cred.json"

    @property
    def x_cookies_path(self) -> Path:
        return self.cookies_dir / "x_cookies.json"


def _expand_env(value: Any) -> Any:
    if isinstance(value, str):
        return _ENV_PAT.sub(lambda m: os.environ.get(m.group(1), ""), value)
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env(v) for v in value]
    return value


class ConfigError(Exception):
    pass


def load_config(config_path: Path | str | None = None) -> Config:
    """读取 config.yaml，展开 ${ENV}，校验并返回 Config。"""
    load_dotenv()
    path = Path(config_path) if config_path else Path("config.yaml")
    if not path.exists():
        raise ConfigError(f"配置文件不存在：{path}（先运行 python -m bxbot init）")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        raise ConfigError(f"config.yaml 解析失败：{e}") from e
    raw = _expand_env(raw)
    try:
        cfg = Config.model_validate(raw)
    except ValidationError as e:
        raise ConfigError(f"config.yaml 校验失败：\n{e}") from e
    cfg.project_root = path.resolve().parent
    return cfg


def ensure_runtime_dirs(cfg: Config) -> None:
    """创建运行时目录（data/cookies/tmp/logs）。"""
    for d in (cfg.data_dir, cfg.cookies_dir, cfg.tmp_dir, cfg.logs_dir):
        d.mkdir(parents=True, exist_ok=True)
