from __future__ import annotations

import math
from collections import defaultdict
from typing import Any, Iterable, Mapping

from ..chunking import tokenizer_chunks
from ..errors import BackendUnavailableError
from ..models import BackendPrediction


DEFAULT_MODEL = "j-hartmann/emotion-english-distilroberta-base"


def _average(items: Iterable[tuple[Mapping[str, float], int]]) -> dict[str, float]:
    totals: defaultdict[str, float] = defaultdict(float)
    total_weight = 0
    for scores, weight in items:
        safe_weight = max(int(weight), 1)
        total_weight += safe_weight
        for label, score in scores.items():
            totals[label.casefold()] += float(score) * safe_weight
    if not totals or total_weight < 1:
        raise BackendUnavailableError("the Transformers backend returned no emotion scores")
    averaged = {label: value / total_weight for label, value in totals.items()}
    total = sum(averaged.values())
    if not math.isfinite(total) or total <= 0:
        raise BackendUnavailableError("the Transformers backend returned invalid emotion scores")
    return {label: value / total for label, value in sorted(averaged.items())}


class TransformersEmotionBackend:
    name = "transformers"

    def __init__(self, model_name: str = DEFAULT_MODEL, *, allow_download: bool = False) -> None:
        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
        except ImportError as exc:
            raise BackendUnavailableError(
                "Transformers support is optional. Install it with "
                "`pip install 'music-emotion-analysis[transformers]'`."
            ) from exc

        local_only = not allow_download
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=local_only)
            model = AutoModelForSequenceClassification.from_pretrained(model_name, local_files_only=local_only)
        except (OSError, ValueError) as exc:
            gate = " Pass --allow-model-download to permit a Hugging Face download." if local_only else ""
            raise BackendUnavailableError(f"could not load Transformers model {model_name!r}.{gate}") from exc

        self.model_name = model_name
        self.classifier = pipeline(
            task="text-classification",
            model=model,
            tokenizer=self.tokenizer,
            device=-1,
        )

    def predict(self, text: str, *, chunk_size: int = 256) -> BackendPrediction:
        declared_max = int(getattr(self.tokenizer, "model_max_length", 512) or 512)
        if declared_max > 100_000:
            declared_max = 512
        effective_max = min(chunk_size, declared_max)
        chunks = tokenizer_chunks(self.tokenizer, text, effective_max)
        try:
            raw: Any = self.classifier(
                [chunk.text for chunk in chunks],
                top_k=None,
                truncation=True,
            )
        except Exception as exc:
            raise BackendUnavailableError(f"Transformers inference failed: {exc}") from exc

        if raw and isinstance(raw[0], dict):
            raw = [raw]
        if len(raw) != len(chunks):
            raise BackendUnavailableError("Transformers returned an unexpected number of chunk predictions")

        chunk_scores: list[tuple[dict[str, float], int]] = []
