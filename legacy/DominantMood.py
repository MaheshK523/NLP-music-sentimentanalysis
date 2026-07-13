#read song lyrics from csv
#assumes csv has columns: 'title', 'artist', 'lyrics'
df = pd.read_csv('song_lyrics.csv')

batch_size = 5
dominant_moods = []
all_mood_scores = []

for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start+batch_size]
    lyrics_batch = [preprocess_lyrics(text) for text in batch['lyrics']]
    results_batch = mood_classifier(lyrics_batch)

    for i, res in enumerate(results_batch):
        mood_scores = {r['label']: r['score'] for r in res}
        dom_moods = [label for label, score in mood_scores.items() if score >= 0.25]
        if not dom_moods:
            dom_moods = [max(mood_scores, key=mood_scores.get)]
        dominant_moods.append(dom_moods)
        all_mood_scores.append(mood_scores)
        print(f"processed song: {batch.iloc[i]['title']} - dominant moods: {dom_moods}")

df['dominant_moods'] = dominant_moods
df['mood_scores'] = all_mood_scores
df.to_csv('song_lyrics_mood_analysis.csv', index=False)
print("mood analysis completed and saved to song_lyrics_mood_analysis.csv")
