# Methodology

## What the project measures

The tool converts lyric text into a probability-like score distribution over
emotion labels, then selects every label at or above a configurable threshold.
If no label crosses the threshold, the highest-scoring label is selected.
Scores describe the chosen backend; they are not ground-truth interpretations.

## Offline lexicon baseline

`music-emotion-lexicon-v1` is deterministic and has no third-party runtime
dependencies. It tokenizes Unicode letter sequences, case-folds them, and
matches a small, repository-owned English lexicon covering anger, disgust,
fear, joy, neutral, sadness, and surprise. Negators within the preceding two
tokens redirect a match, while a small set of intensifiers scales the next
matched term.

Each chunk starts with smoothing weights so unknown text remains valid rather
than producing an empty result. Chunk distributions are averaged by token
