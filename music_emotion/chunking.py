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
