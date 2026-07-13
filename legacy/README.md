# Legacy prototype

These files are preserved verbatim from the original repository history. They
are not imported by the maintained package and are not presented as a complete
or reproducible pipeline.

| File | First repository commit | Commit timestamp |
|---|---|---|
| `SentimentAnalysisPreProcess.py` | `11e49a46e779222de5fdce8f199706d8dc1e0c2a` | `2025-09-24T22:16:05-07:00` |
| `DominantMood.py` | `9914bd69f30d6d5290e4155fb4b258c570c3e9fa` | `2025-09-24T22:17:26-07:00` |
| `Visualization.py` | `ffbc3e3cb9ec4b6909d20a7838743a371493b779` | `2025-09-24T22:18:27-07:00` |
| `Radar_Chart.py` | `12e0c7042ce9b93df4e61d8cb32ba1ed06e719a3` | `2025-09-24T22:27:49-07:00` |

The scripts relied on shared global state, omitted several imports, loaded a
large model during module import, serialized Python dictionaries directly into
CSV cells, and had no long-text policy or tests. They remain here for provenance
and comparison only. Use `python -m music_emotion` or the `music-emotion`
console command for maintained workflows.
