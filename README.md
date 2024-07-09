# Music Emotion Analysis

An offline-first Python toolkit for turning lyric datasets into structured,
reviewable emotion profiles. It includes a deterministic zero-dependency
baseline, validated CSV and JSONL ingestion, long-text chunking, stable JSON
scores, a gated Transformers adapter, and self-contained HTML reports.

The project analyzes **lyrics**, not audio. Its outputs are backend estimates,
not objective readings of a song or claims about an artist's mental state.

## Quick start

Python 3.10 or newer is required. The default workflow needs no model download
and no runtime dependency outside the standard library.

```bash
python -m pip install -e .

music-emotion analyze examples/sample_songs.csv \
  --output output/analysis.csv \
