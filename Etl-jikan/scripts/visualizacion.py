import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/top_anime.csv")

plt.figure(figsize=(10,6))
plt.barh(df["title"][:10], df["score"][:10])
plt.xlabel("Score")
plt.title("Top 10 Anime")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("data/grafico.png")
plt.show()