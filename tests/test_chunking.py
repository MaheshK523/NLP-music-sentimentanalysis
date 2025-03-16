import unittest

from music_emotion.chunking import tokenizer_chunks, tokenize_words, word_chunks


class FakeTokenizer:
    def num_special_tokens_to_add(self, pair=False):
        return 2

    def encode(self, text, add_special_tokens=False):
