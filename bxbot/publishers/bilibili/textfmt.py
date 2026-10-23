"""发布正文排版：译文 + 原文 + 原推链接 + hashtag → B 站标签/话题转换。"""

from __future__ import annotations

import re

SEPARATOR = "\n\n——原推——\n"

# Twitter hashtag：# 后跟字母/数字/下划线/中文（排除 URL 锚点：前面不能是字母数字/斜杠）
_HASHTAG_PAT = re.compile(r"(?<![\w/])#([A-Za-z0-9_一-鿿]+)")


def extract_hashtags(text: str) -> list[str]:
    """提取推文中的 hashtag（保序去重）。"""
    seen: set[str] = set()
    out: list[str] = []
    for tag in _HASHTAG_PAT.findall(text or ""):
        if tag.lower() not in seen:
            seen.add(tag.lower())
            out.append(tag)
    return out


def strip_hashtags(text: str) -> str:
    """从文本中移除 hashtag（连同前导空格）。"""
    cleaned = re.sub(r"[ \t]*#[A-Za-z0-9_一-鿿]+", "", text or "")
    return re.sub(r"[ \t]+\n", "\n", cleaned).strip()


def bili_topics_suffix(tags: list[str], max_topics: int = 5) -> str:
    """把标签转为 B 站动态话题格式后缀：#话题1# #话题2#（无标签返回空串）。"""
    topics = [t for t in tags if t][:max_topics]
    return " ".join(f"#{t}#" for t in topics)


# 图片类链接（pic 预览 / 推文照片页）：图片已上传 B 站，链接本身冗余，从正文移除
_MEDIA_LINK_PAT = re.compile(r"^https?://pic\.twitter\.com/|/status/\d+/photo")


def expand_tco_links(text: str, url_entities: dict[str, str] | None) -> str:
    """t.co 短链替换为真实链接；图片类链接直接移除。"""
    for tco, expanded in (url_entities or {}).items():
        if not tco or tco not in text:
            continue
        if _MEDIA_LINK_PAT.search(expanded or ""):
            text = re.sub(r"[ \t]*" + re.escape(tco), "", text)
        else:
            text = text.replace(tco, expanded or tco)
    return text.strip()


def render_body(
    translate: str,
    original: str,
    url: str,
    *,
    mode: str = "both",
    always_include_source_link: bool = True,
    max_len: int = 2000,
) -> str:
    """mode: both | translated_only | original_only。超长时优先保链接、截译文。"""
    parts: list[str] = []
    if mode in ("both", "translated_only") and translate:
        parts.append(translate.strip())
    if mode in ("both", "original_only") and original:
        parts.append("——原推——\n" + original.strip())

    body = "\n\n".join(parts)
    link = f"🔗 {url}"

    if always_include_source_link or mode == "both":
        candidate = body + "\n\n" + link
    else:
        candidate = body

    if len(candidate) <= max_len:
        return candidate

    # 超长：保留链接，截断正文（… 占 1 字符）
    budget = max_len - len(link) - 3
    if budget < 1:
        return link[:max_len]
    truncated = body[:budget].rstrip() + "…"
    return truncated + "\n\n" + link


def make_video_title(
    translate: str, fallback_handle: str = "", max_len: int = 80
) -> str:
    """视频稿件标题：译文首行截断，去换行。"""
    first_line = (translate or "").strip().splitlines()[0] if translate.strip() else ""
    title = first_line.replace("\n", " ").strip() or f"@{fallback_handle} 的新推文"
    return title[:max_len].rstrip()
