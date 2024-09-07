import numpy as np
import os

#function to plot radar chart for a single song
def plot_song_radar(song_title, mood_scores, save_dir="mood_charts"):
    os.makedirs(save_dir, exist_ok=True)
    labels = list(mood_scores.keys())
    values = list(mood_scores.values())
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_title(f"Mood profile: {song_title}", size=14, weight='bold')
    filename = os.path.join(save_dir, f"{re.sub(r'[^a-zA-Z0-9]', '_', song_title)}.png")
    plt.savefig(filename)
    plt.close()
    print(f"saved radar chart for {song_title} -> {filename}")

#generate and save radar chart for every song
for idx in range(len(df)):
    title = df.iloc[idx]['title']
    scores = df.iloc[idx]['mood_scores']
    plot_song_radar(title, scores)
