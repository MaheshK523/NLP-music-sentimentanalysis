from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .analysis import analyze_records
from .backends import create_backend
from .errors import MusicEmotionError
from .io import load_songs, write_results
from .report import generate_report, load_analysis_results


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="music-emotion",
        description="Analyze lyric emotion with an offline baseline or an explicitly enabled Transformers model.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="analyze a validated CSV or JSONL dataset")
    analyze.add_argument("input", type=Path)
    analyze.add_argument("-o", "--output", type=Path, required=True)
    analyze.add_argument("--input-format", choices=("auto", "csv", "jsonl"), default="auto")
    analyze.add_argument("--output-format", choices=("auto", "csv", "jsonl"), default="auto")
    analyze.add_argument("--backend", choices=("lexicon", "transformers"), default="lexicon")
    analyze.add_argument("--model", help="Hugging Face model ID for the Transformers backend")
    analyze.add_argument(
        "--allow-model-download",
        action="store_true",
        help="allow the explicitly selected Transformers backend to download model files",
    )
    analyze.add_argument("--threshold", type=float, default=0.25)
    analyze.add_argument("--chunk-size", type=int, default=256)
    analyze.add_argument("--report-dir", type=Path, help="also write HTML, Markdown, and JSON summaries")

    report = subparsers.add_parser("report", help="build reports from a prior analysis CSV or JSONL")
    report.add_argument("input", type=Path)
