import matplotlib.pyplot as plt

#aggregate visualization
mood_counts = {}
for moods in dominant_moods:
    for mood in moods:
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

plt.figure(figsize=(8,6))
plt.bar(mood_counts.keys(), mood_counts.values())
plt.title("distribution of dominant moods across songs")
plt.xlabel("mood")
plt.ylabel("count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("mood_distribution.png")
plt.close()
print("saved overall mood distribution as mood_distribution.png")
