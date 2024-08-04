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
  --report-dir output/report
```

Open `output/report/report.html` to explore the aggregate score profile and
per-song results. The report directory also contains Markdown and machine-
readable JSON summaries.

JSONL works in both directions:

```bash
music-emotion analyze examples/sample_songs.jsonl \
  --output output/analysis.jsonl

music-emotion report output/analysis.jsonl \
  --output-dir output/rebuilt-report
```

## Input and output contract

Every input record must contain non-empty string values for:

| Field | Meaning |
|---|---|
| `title` | Song or text title |
| `artist` | Artist, author, or dataset attribution |
| `lyrics` | Text to analyze |

Additional fields are preserved. Malformed JSON, missing CSV headers, duplicate
columns, blank required values, and non-string JSON fields fail with row-aware
messages.

Outputs add:

| Field | Encoding |
|---|---|
| `dominant_emotions` | JSON array; also JSON-encoded inside CSV |
| `emotion_scores` | JSON object with normalized scores; JSON-encoded inside CSV |
| `analysis_backend` | `lexicon` or `transformers` |
| `analysis_model` | Backend/model identifier |
| `chunk_count` | Number of chunks included in aggregation |

Python dictionary representations are never written into interchange files.

## Backends

### Deterministic offline baseline

`--backend lexicon` is the default. It uses an inspectable English emotion
lexicon, simple negation/intensifier handling, word-aware chunking, and weighted
aggregation. It is useful for reproducible demos, integration tests, and a
transparent baseline. It is not a learned state-of-the-art classifier.

```bash
music-emotion analyze songs.csv -o analysis.csv \
  --backend lexicon --threshold 0.25 --chunk-size 256
```

### Optional Transformers inference

Transformers and PyTorch are deliberately optional:

```bash
python -m pip install -e '.[transformers]'

music-emotion analyze songs.csv -o analysis.jsonl \
  --backend transformers \
  --model j-hartmann/emotion-english-distilroberta-base \
  --allow-model-download
```

