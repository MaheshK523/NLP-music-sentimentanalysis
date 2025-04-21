# Methodology

## What the project measures

The tool converts lyric text into a probability-like score distribution over
emotion labels, then selects every label at or above a configurable threshold.
If no label crosses the threshold, the highest-scoring label is selected.
Scores describe the chosen backend; they are not ground-truth interpretations.

## Offline lexicon baseline
