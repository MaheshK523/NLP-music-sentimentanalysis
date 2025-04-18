import pandas as pd
import re
from transformers import pipeline

#load emotion detection pipeline
mood_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

#function to preprocess lyrics
def preprocess_lyrics(text):
    text = text.lower()
