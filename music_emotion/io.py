from __future__ import annotations

import csv
import json
import os
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, TextIO

from .errors import DataValidationError
from .models import AnalysisResult, SongRecord


INPUT_FIELDS = ("title", "artist", "lyrics")
RESULT_FIELDS = (
    "dominant_emotions",
    "emotion_scores",
    "analysis_backend",
    "analysis_model",
    "chunk_count",
)
RESERVED_FIELDS = set(INPUT_FIELDS + RESULT_FIELDS)


def infer_format(path: str | Path, selected: str = "auto") -> str:
    if selected != "auto":
        return selected
    suffix = Path(path).suffix.casefold()
    if suffix == ".csv":
        return "csv"
    if suffix in {".jsonl", ".ndjson"}:
        return "jsonl"
    raise DataValidationError("could not infer format; use a .csv/.jsonl path or pass an explicit format")


def _validate_song(row: Mapping[str, Any], source_row: int) -> SongRecord:
    missing = [field for field in INPUT_FIELDS if field not in row]
    if missing:
        raise DataValidationError(f"row {source_row}: missing required field(s): {', '.join(missing)}")

    values: dict[str, str] = {}
    for field in INPUT_FIELDS:
        value = row[field]
        if not isinstance(value, str):
            raise DataValidationError(f"row {source_row}: {field!r} must be a string")
        if not value.strip():
            raise DataValidationError(f"row {source_row}: {field!r} cannot be blank")
        values[field] = value.strip() if field != "lyrics" else value

    extra = {str(key): value for key, value in row.items() if key not in INPUT_FIELDS and key is not None}
    return SongRecord(**values, extra=extra, source_row=source_row)


def _load_csv(handle: TextIO) -> list[SongRecord]:
    reader = csv.DictReader(handle)
    if reader.fieldnames is None:
        raise DataValidationError("CSV input must include a header row")
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise DataValidationError("CSV input contains duplicate column names")
    missing = [field for field in INPUT_FIELDS if field not in reader.fieldnames]
    if missing:
        raise DataValidationError(f"CSV header is missing: {', '.join(missing)}")
    records = [_validate_song(row, source_row=index) for index, row in enumerate(reader, start=2)]
    if not records:
        raise DataValidationError("input dataset contains no songs")
    return records


def _load_jsonl(handle: TextIO) -> list[SongRecord]:
    records: list[SongRecord] = []
    for line_number, line in enumerate(handle, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DataValidationError(f"line {line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(row, dict):
            raise DataValidationError(f"line {line_number}: each JSONL value must be an object")
        records.append(_validate_song(row, source_row=line_number))
    if not records:
        raise DataValidationError("input dataset contains no songs")
    return records


def load_songs(path: str | Path, *, input_format: str = "auto") -> list[SongRecord]:
    source = Path(path)
    selected = infer_format(source, input_format)
    try:
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            return _load_csv(handle) if selected == "csv" else _load_jsonl(handle)
    except OSError as exc:
        raise DataValidationError(f"could not read {source}: {exc}") from exc


def _csv_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple, bool)) or value is None:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def result_mapping(result: AnalysisResult, *, json_native: bool) -> dict[str, Any]:
    extra = {key: value for key, value in result.song.extra.items() if key not in RESERVED_FIELDS}
    scores = {key: round(float(value), 10) for key, value in sorted(result.emotion_scores.items())}
    dominant = list(result.dominant_emotions)
    row: dict[str, Any] = {
        "title": result.song.title,
        "artist": result.song.artist,
        "lyrics": result.song.lyrics,
        **extra,
        "dominant_emotions": dominant,
        "emotion_scores": scores,
        "analysis_backend": result.backend,
        "analysis_model": result.model,
        "chunk_count": result.chunk_count,
    }
    return row if json_native else {key: _csv_value(value) for key, value in row.items()}


def _atomic_replace(path: Path, write: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        write(temporary)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_results(
    results: Iterable[AnalysisResult],
    path: str | Path,
    *,
    output_format: str = "auto",
) -> int:
    target = Path(path)
    selected = infer_format(target, output_format)
    materialized = list(results)
    if not materialized:
        raise DataValidationError("cannot write an empty analysis result")

    if selected == "jsonl":
        def write_jsonl(temporary: Path) -> None:
            with temporary.open("w", encoding="utf-8", newline="\n") as handle:
                for result in materialized:
                    handle.write(json.dumps(result_mapping(result, json_native=True), ensure_ascii=False, sort_keys=True))
                    handle.write("\n")

        _atomic_replace(target, write_jsonl)
        return len(materialized)
