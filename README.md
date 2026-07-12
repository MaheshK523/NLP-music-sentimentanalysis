# Music Emotion Analysis

A Python prototype that maps song lyrics to emotion scores and produces dataset-level and per-song visualizations.

The project uses the existing Hugging Face checkpoint `j-hartmann/emotion-english-distilroberta-base`. The model is loaded for inference; this repository does not train or fine-tune DistilRoBERTa.

## Pipeline

1. Convert lyrics to lowercase.
2. Remove non-letter characters and collapse repeated whitespace.
3. Run the text through the pretrained emotion-classification pipeline.
4. Retain every emotion at or above a configurable threshold (`0.25` by default).
5. Fall back to the highest-scoring emotion when no score crosses the threshold.
6. Add dominant-emotion and full-score columns to a CSV dataset.
7. Generate an aggregate bar chart and one radar chart per song.

The expected input described by the scripts is `song_lyrics.csv`, with title, artist, and lyrics fields. The annotated output is written as `song_lyrics_mood_analysis.csv`.

## Repository map

| File | Purpose |
|---|---|
| [`SentimentAnalysisPreProcess.py`](SentimentAnalysisPreProcess.py) | Text cleanup and model inference |
| [`DominantMood.py`](DominantMood.py) | Batch processing and dominant-emotion selection |
| [`Visualization.py`](Visualization.py) | Dataset-level emotion distribution |
| [`Radar_Chart.py`](Radar_Chart.py) | Per-song radar charts |
| [`requirements`](requirements) | Python dependency list |

## Outputs

The batch pipeline adds:

- `dominant_moods`: emotions that meet the selected threshold;
- `mood_scores`: the complete classifier score mapping.

Visualization scripts produce:

- `mood_distribution.png` for aggregate dominant-emotion counts;
- files under `mood_charts/` for per-song score profiles.

## Limitations

- The checkpoint is an existing English emotion classifier, not a model trained on this repository's song-lyrics data.
- Classifier scores are model outputs, not objective measurements of a song's emotional meaning.
- The `0.25` cutoff is a heuristic and has not been calibrated against a labeled evaluation set in this repository.
- Lowercasing and removing punctuation or non-ASCII letters may discard useful signals, especially for multilingual lyrics, names, contractions, and stylistic punctuation.
- The code does not define a chunking or truncation policy for lyrics that exceed the classifier's input length.
- No labeled dataset, train/test split, accuracy measurement, error analysis, or human evaluation is included.
- The scripts are separate modules rather than one documented command-line entry point.

## Data and usage rights

No lyric dataset is checked into the repository. Anyone using the pipeline is responsible for ensuring they have permission to process and store the lyrics they provide, as well as for following the pretrained model's license and usage terms.
