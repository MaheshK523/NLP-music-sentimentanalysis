import pandas as pd
import re
from transformers import pipeline

#load emotion detection pipeline
mood_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

#function to preprocess lyrics
def preprocess_lyrics(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

#function to get moods and scores
def get_song_mood(lyrics, threshold=0.25):
    lyrics_clean = preprocess_lyrics(lyrics)
    results = mood_classifier(lyrics_clean)
    mood_scores = {res['label']: res['score'] for res in results[0]}
    dominant_moods = [label for label, score in mood_scores.items() if score >= threshold]
    if not dominant_moods:
        dominant_moods = [max(mood_scores, key=mood_scores.get)]
    return dominant_moods, mood_scores
