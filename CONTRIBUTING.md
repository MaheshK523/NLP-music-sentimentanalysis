# Contributing

1. Create a virtual environment and install the package with `pip install -e .`.
2. Run `python -m unittest discover -s tests -v` before opening a change.
3. Keep the default path offline and dependency-free.
4. Add validation and failure-case tests for schema or CLI changes.
5. Do not add copyrighted lyric datasets, downloaded checkpoints, or model
   caches. Synthetic fixtures must be labeled as such.

Changes to the lexicon or aggregation policy alter model behavior. Update the
model name/version, methodology document, and tests together.
