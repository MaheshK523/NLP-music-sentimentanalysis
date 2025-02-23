from __future__ import annotations

from .base import EmotionBackend
from .lexicon import LexiconEmotionBackend


def create_backend(
    name: str,
    *,
    model_name: str | None = None,
    allow_download: bool = False,
) -> EmotionBackend:
    normalized = name.casefold()
    if normalized == "lexicon":
        return LexiconEmotionBackend()
    if normalized == "transformers":
        from .transformers import DEFAULT_MODEL, TransformersEmotionBackend

        return TransformersEmotionBackend(model_name or DEFAULT_MODEL, allow_download=allow_download)
    raise ValueError(f"unknown backend: {name}")


__all__ = ["EmotionBackend", "LexiconEmotionBackend", "create_backend"]
