import requests
import pandas as pd
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract():
    url = "https://api.jikan.moe/v4/top/anime"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["data"]

def transform(data):
    registros = []
    for item in data:
        registros.append({
            "mal_id": item["mal_id"],
            "title": item["title"],
            "score": item["score"],
            "episodes": item["episodes"],
            "members": item["members"],
            "fecha_extraccion": datetime.now()
        })
    return pd.DataFrame(registros)

def load(df):
    df.to_csv("data/top_anime.csv", index=False)
    logging.info("Datos guardados correctamente")

def main():
    try:
        data = extract()
        df = transform(data)
        load(df)
        print(df.head())
    except Exception as e:
        logging.error(f"Error: {e}")
        print("Error en ejecución")

if __name__ == "__main__":
    main()