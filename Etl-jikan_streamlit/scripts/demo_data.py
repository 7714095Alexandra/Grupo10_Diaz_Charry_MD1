import pandas as pd
import random

titulos = [
    "Naruto", "One Piece", "Attack on Titan", "Death Note",
    "Demon Slayer", "Jujutsu Kaisen", "Fullmetal Alchemist",
    "Tokyo Ghoul", "My Hero Academia", "Dragon Ball"
]

temporadas = ["Winter", "Spring", "Summer", "Fall"]
estados = ["Finished Airing", "Currently Airing"]

generos_lista = [
    "Action", "Adventure", "Drama", "Fantasy",
    "Comedy", "Horror", "Romance", "Sci-Fi"
]

data = []

for i in range(1000):
    titulo = random.choice(titulos)

    data.append({
        "mal_id": i + 1,
        "titulo": f"{titulo} {i}",  # para evitar duplicados
        "score": round(random.uniform(5, 10), 2),
        "episodios": random.randint(1, 100),
        "estado": random.choice(estados),
        "anio": random.randint(2000, 2024),
        "temporada": random.choice(temporadas),
        "genero": random.choice(generos_lista),
        "popularidad": random.randint(1, 10000),
        "ranking": random.randint(1, 5000),
        "miembros": random.randint(1000, 1000000),
        "favoritos": random.randint(100, 50000)
    })

df = pd.DataFrame(data)

# guardar archivo
df.to_csv("data_anime.csv", index=False)

print("✅ 1000 registros de anime generados en data_anime.csv")