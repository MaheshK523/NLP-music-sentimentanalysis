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
    report.add_argument("-o", "--output-dir", type=Path, required=True)
    report.add_argument("--input-format", choices=("auto", "csv", "jsonl"), default="auto")
    return parser


def _run_analyze(args: argparse.Namespace) -> int:
    if args.allow_model_download and args.backend != "transformers":
        raise MusicEmotionError("--allow-model-download only applies to --backend transformers")
    records = load_songs(args.input, input_format=args.input_format)
    backend = create_backend(args.backend, model_name=args.model, allow_download=args.allow_model_download)
    results = list(
        analyze_records(
            records,
            backend,
            threshold=args.threshold,
            chunk_size=args.chunk_size,
        )
    )
    count = write_results(results, args.output, output_format=args.output_format)
    print(f"Analyzed {count} song(s) with {backend.name}; wrote {args.output}")
    if args.report_dir:
        artifacts = generate_report(results, args.report_dir)
        print(f"Report: {artifacts.html}")
    return 0


def _run_report(args: argparse.Namespace) -> int:
    results = load_analysis_results(args.input, input_format=args.input_format)
    artifacts = generate_report(results, args.output_dir)
    print(f"Reported on {len(results)} song(s); wrote {artifacts.html}")
