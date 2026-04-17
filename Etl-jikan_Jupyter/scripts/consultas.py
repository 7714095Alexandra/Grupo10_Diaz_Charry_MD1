#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from scripts.database import SessionLocal
from sqlalchemy import func
import pandas as pd

# ⚠️ IMPORTA tus modelos reales
from scripts.models import Anime  # <- ajusta si tu modelo tiene otro nombre

db = SessionLocal()

def top_animes():
    """Top animes por score"""
    registros = db.query(
        Anime.titulo,
        Anime.score
    ).order_by(Anime.score.desc()).limit(10).all()

    df = pd.DataFrame(registros, columns=['Anime', 'Score'])
    print("\n🏆 TOP 10 ANIMES:")
    print(df.to_string(index=False))




def animes_mas_populares():
    """Animes con más popularidad"""
    registros = db.query(
        Anime.titulo,
        Anime.popularity
    ).order_by(Anime.popularity.asc()).limit(10).all()

    df = pd.DataFrame(registros, columns=['Anime', 'Popularidad'])
    print("\n🔥 ANIMES MÁS POPULARES:")
    print(df.to_string(index=False))
  


def total_animes():
    """Total de animes guardados"""
    total = db.query(func.count(Anime.id)).scalar()
    print(f"\n📊 TOTAL DE ANIMES EN BD: {total}")


if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("ANÁLISIS DE DATOS - ANIME (JIKAN)")
        print("="*50)

        total_animes()
        top_animes()
        animes_mas_populares()

        print("\n" + "="*50 + "\n")

    finally:
        db.close()