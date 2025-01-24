from __future__ import annotations

import html
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .errors import DataValidationError
from .io import load_songs
from .models import AnalysisResult


@dataclass(frozen=True, slots=True)
class ReportArtifacts:
    html: Path
    markdown: Path
    summary_json: Path


def _parse_json_value(value: Any, expected: type, field: str, row: int | None) -> Any:
    parsed = value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise DataValidationError(f"row {row}: {field} must contain valid JSON") from exc
    if not isinstance(parsed, expected):
        raise DataValidationError(f"row {row}: {field} must be a JSON {expected.__name__}")
    return parsed


def load_analysis_results(path: str | Path, *, input_format: str = "auto") -> list[AnalysisResult]:
    songs = load_songs(path, input_format=input_format)
    results: list[AnalysisResult] = []
    for song in songs:
        missing = [field for field in ("dominant_emotions", "emotion_scores") if field not in song.extra]
        if missing:
            raise DataValidationError(f"row {song.source_row}: missing analysis field(s): {', '.join(missing)}")
        dominant = _parse_json_value(song.extra["dominant_emotions"], list, "dominant_emotions", song.source_row)
        scores = _parse_json_value(song.extra["emotion_scores"], dict, "emotion_scores", song.source_row)
        if not dominant or not all(isinstance(label, str) and label.strip() for label in dominant):
            raise DataValidationError(f"row {song.source_row}: dominant_emotions must contain labels")
        clean_scores: dict[str, float] = {}
        for label, value in scores.items():
            try:
                score = float(value)
            except (TypeError, ValueError) as exc:
                raise DataValidationError(f"row {song.source_row}: invalid score for {label!r}") from exc
            if not math.isfinite(score) or not 0 <= score <= 1:
                raise DataValidationError(f"row {song.source_row}: scores must be finite values from 0 to 1")
            clean_scores[str(label)] = score
        if not clean_scores:
            raise DataValidationError(f"row {song.source_row}: emotion_scores cannot be empty")
        try:
            chunk_count = int(song.extra.get("chunk_count", 1))
        except (TypeError, ValueError) as exc:
            raise DataValidationError(f"row {song.source_row}: chunk_count must be an integer") from exc
        results.append(
            AnalysisResult(
                song=song,
                dominant_emotions=tuple(dominant),
                emotion_scores=clean_scores,
                backend=str(song.extra.get("analysis_backend", "unknown")),
                model=str(song.extra.get("analysis_model", "unknown")),
                chunk_count=chunk_count,
            )
        )
    return results


def summarize(results: Iterable[AnalysisResult]) -> dict[str, Any]:
    materialized = list(results)
    if not materialized:
        raise DataValidationError("cannot report on an empty result set")
    dominant_counts: Counter[str] = Counter()
    score_totals: defaultdict[str, float] = defaultdict(float)
    for result in materialized:
        dominant_counts.update(result.dominant_emotions)
        for label, score in result.emotion_scores.items():
            score_totals[label] += float(score)
    labels = sorted(score_totals)
    return {
        "schema_version": 1,
        "song_count": len(materialized),
        "backend_counts": dict(sorted(Counter(result.backend for result in materialized).items())),
        "model_counts": dict(sorted(Counter(result.model for result in materialized).items())),
        "dominant_emotion_counts": dict(sorted(dominant_counts.items(), key=lambda item: (-item[1], item[0]))),
        "average_emotion_scores": {label: round(score_totals[label] / len(materialized), 10) for label in labels},
    }


def _markdown(results: list[AnalysisResult], summary: Mapping[str, Any]) -> str:
    lines = [
        "# Music emotion analysis report",
        "",
        f"Songs analyzed: **{summary['song_count']}**",
        "",
        "## Dominant emotions",
        "",
        "| Emotion | Songs |",
        "|---|---:|",
    ]
    lines.extend(f"| {label} | {count} |" for label, count in summary["dominant_emotion_counts"].items())
    lines.extend(["", "## Average scores", "", "| Emotion | Mean score |", "|---|---:|"])
    lines.extend(f"| {label} | {score:.3f} |" for label, score in summary["average_emotion_scores"].items())
    lines.extend(["", "## Songs", "", "| Title | Artist | Dominant emotion(s) | Chunks |", "|---|---|---|---:|"])
    for result in results:
        title = result.song.title.replace("|", "\\|")
        artist = result.song.artist.replace("|", "\\|")
        lines.append(f"| {title} | {artist} | {', '.join(result.dominant_emotions)} | {result.chunk_count} |")
    lines.extend(
        [
            "",
            "> Scores describe the selected backend's output. They are not objective labels or clinical measurements.",
            "",
        ]
    )
    return "\n".join(lines)


def _html(results: list[AnalysisResult], summary: Mapping[str, Any]) -> str:
    dominant_cards = "".join(
        f'<div class="metric"><span>{html.escape(label.title())}</span><strong>{count}</strong></div>'
        for label, count in summary["dominant_emotion_counts"].items()
    )
    average_bars = "".join(
        "<div class=\"bar-row\"><span>{}</span><div class=\"track\"><i style=\"width:{:.2f}%\"></i></div><b>{:.3f}</b></div>".format(
            html.escape(label.title()), score * 100, score
        )
        for label, score in summary["average_emotion_scores"].items()
    )
    rows = []
    for result in results:
        top_scores = sorted(result.emotion_scores.items(), key=lambda item: (-item[1], item[0]))[:3]
        score_text = ", ".join(f"{label} {score:.2f}" for label, score in top_scores)
        rows.append(
            "<tr><td><strong>{}</strong><small>{}</small></td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                html.escape(result.song.title),
                html.escape(result.song.artist),
                html.escape(", ".join(result.dominant_emotions)),
                html.escape(score_text),
                result.chunk_count,
            )
        )
    return f"""<!doctype html>
<html lang="en">
<head>
