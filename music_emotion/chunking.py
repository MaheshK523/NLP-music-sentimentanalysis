from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)


@dataclass(frozen=True, slots=True)
class TextChunk:
    text: str
    weight: int


def tokenize_words(text: str) -> list[str]:
    return [match.group(0).casefold().replace("’", "'") for match in WORD_RE.finditer(text)]


def word_chunks(text: str, max_words: int) -> list[TextChunk]:
    if max_words < 1:
        raise ValueError("max_words must be at least 1")
    words = tokenize_words(text)
    if not words:
        return [TextChunk(text="", weight=1)]
    return [
        TextChunk(text=" ".join(words[start : start + max_words]), weight=len(words[start : start + max_words]))
        for start in range(0, len(words), max_words)
    ]


def tokenizer_chunks(tokenizer: Any, text: str, max_tokens: int) -> list[TextChunk]:
    """Split text on model token IDs while reserving required special tokens."""
    if max_tokens < 2:
        raise ValueError("max_tokens must be at least 2")
    special_tokens = 0
    if hasattr(tokenizer, "num_special_tokens_to_add"):
        special_tokens = int(tokenizer.num_special_tokens_to_add(pair=False))
    payload_size = max_tokens - special_tokens
    if payload_size < 1:
        raise ValueError("max_tokens is too small for the tokenizer's special tokens")

    token_ids = list(tokenizer.encode(text, add_special_tokens=False))
    if not token_ids:
        return [TextChunk(text="", weight=1)]

    chunks: list[TextChunk] = []
    for start in range(0, len(token_ids), payload_size):
        ids = token_ids[start : start + payload_size]
