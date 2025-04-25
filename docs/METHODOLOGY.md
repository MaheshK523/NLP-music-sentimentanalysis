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
count and normalized to sum to one. This is an inspectable smoke-test baseline,
not a trained classifier and not a substitute for human annotation.

## Long-text handling

The lexicon backend chunks by normalized words. The optional Transformers
backend uses the selected tokenizer's token IDs, reserves the tokenizer's
special-token budget, and decodes non-overlapping chunks that fit within both
the requested size and the model's declared maximum length. Per-chunk model
distributions are averaged by model-token count.

This avoids silently truncating an entire lyric to its opening segment. The
current aggregation does not model narrative order across chunks.

## Determinism

The lexicon backend performs no random sampling, network access, or model
download. Given the same package version, text, chunk size, and threshold, its
output is deterministic. JSON keys and CSV score objects are serialized in a
stable order.
