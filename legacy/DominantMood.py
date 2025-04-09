#read song lyrics from csv
#assumes csv has columns: 'title', 'artist', 'lyrics'
df = pd.read_csv('song_lyrics.csv')

batch_size = 5
dominant_moods = []
all_mood_scores = []

for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start+batch_size]
