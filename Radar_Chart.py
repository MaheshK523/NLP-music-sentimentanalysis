import numpy as np
import os

#function to plot radar chart for a single song
def plot_song_radar(song_title, mood_scores, save_dir="mood_charts"):
    os.makedirs(save_dir, exist_ok=True)
    labels = list(mood_scores.keys())
    values = list(mood_scores.values())
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
