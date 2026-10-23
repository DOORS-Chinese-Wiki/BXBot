"""DryRunPublisher：只打印将要发布的内容，绝不外发。"""

from __future__ import annotations

from bxbot.models import PublishBundle, PublishResult


def _preview(bundle: PublishBundle, kind: str, extra: str = "") -> str:
    return "\n".join(
        [
            f"──── DRY-RUN [{kind}] ────",
            f"tweet: {bundle.tweet.url}",
            f"title: {bundle.title}",
            f"tags:  {','.join(bundle.tags)}",
            f"tid:   {bundle.tid}",
            f"body:\n{bundle.text_final}",
            f"media: {len(bundle.media_files)} 个本地文件"
            + (
                f" -> {[str(p) for p in bundle.media_files]}"
                if bundle.media_files
                else ""
            ),
            f"cover: {bundle.cover_path or '-'}",
            f"llm:   should_sync={bundle.llm.should_sync} reason={bundle.llm.reason or '-'}",
            (extra or ""),
            "──────────────────────────",
        ]
    )


class DryRunPublisher:
    async def publish_video(self, bundle: PublishBundle) -> PublishResult:
        preview = _preview(bundle, "video 稿件", "bili_api: VideoUploader.start()")
        print(preview)
        return PublishResult(ok=True, kind="dry_run", dry_run_preview=preview)

    async def publish_image_dynamic(self, bundle: PublishBundle) -> PublishResult:
        preview = _preview(bundle, "图文动态", "bili_api: dynamic.send_dynamic(图片)")
        print(preview)
        return PublishResult(ok=True, kind="dry_run", dry_run_preview=preview)

    async def publish_text_dynamic(self, bundle: PublishBundle) -> PublishResult:
        preview = _preview(bundle, "文字动态", "bili_api: dynamic.send_dynamic(纯文本)")
        print(preview)
        return PublishResult(ok=True, kind="dry_run", dry_run_preview=preview)
