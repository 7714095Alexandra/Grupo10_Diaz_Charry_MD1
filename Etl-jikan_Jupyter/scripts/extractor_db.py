#!/usr/bin/env python3
import os
import requests
import time
from dotenv import load_dotenv
import logging

from scripts.database import SessionLocal
from scripts.models import Anime, MetricasETL, Genero, AnimeGenero

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class JikanETL:

    def __init__(self):
        self.base_url = os.getenv('JIKAN_BASE_URL')
        self.db = SessionLocal()

        self.tiempo_inicio = time.time()
        self.registros_extraidos = 0
        self.registros_guardados = 0
        self.registros_fallidos = 0

        if not self.base_url:
            raise ValueError("JIKAN_BASE_URL no configurada")

    def extraer_animes(self, page=1):
        try:
            url = f"{self.base_url}/anime"
            params = {"page": page}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            animes = data.get('data', [])

            self.registros_extraidos += len(animes)

            logger.info(f"✅ Página {page} extraída")
            return animes

        except Exception as e:
            logger.error(f"❌ Error extrayendo página {page}: {e}")
            self.registros_fallidos += 1
            return []

    def procesar_anime(self, anime):
        return {
            "titulo": anime.get("title"),
            "tipo": anime.get("type"),
            "episodios": anime.get("episodes"),
            "score": anime.get("score"),
            "popularity": anime.get("popularity"),
            "miembros": anime.get("members"),
            "estado": anime.get("status"),
            "fecha_emision": str(anime.get("aired", {}).get("string")),
            "generos": [g["name"] for g in anime.get("genres", [])]
        }

    def guardar_en_bd(self, datos):
        try:
            # 🔹 Guardar anime
            anime = Anime(
                titulo=datos["titulo"],
                tipo=datos["tipo"],
                episodios=datos["episodios"],
                score=datos["score"],
                popularity=datos["popularity"],
                miembros=datos["miembros"],
                estado=datos["estado"],
                fecha_emision=datos["fecha_emision"]
            )

            self.db.add(anime)
            self.db.commit()
            self.db.refresh(anime)

            # 🔹 Guardar géneros
            for genero_nombre in datos.get("generos", []):

                genero = self.db.query(Genero).filter_by(nombre=genero_nombre).first()

                if not genero:
                    genero = Genero(nombre=genero_nombre)
                    self.db.add(genero)
                    self.db.commit()
                    self.db.refresh(genero)

                relacion = AnimeGenero(
                    anime_id=anime.id,
                    genero_id=genero.id
                )

                self.db.add(relacion)

            self.db.commit()

            self.registros_guardados += 1
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error guardando anime: {e}")
            self.registros_fallidos += 1
            return False

    def guardar_metricas(self, estado):
        try:
            tiempo = time.time() - self.tiempo_inicio

            metricas = MetricasETL(
                registros_extraidos=self.registros_extraidos,
                registros_guardados=self.registros_guardados,
                registros_fallidos=self.registros_fallidos,
                tiempo_ejecucion_segundos=tiempo,
                estado=estado,
                mensaje=f"Extraídos: {self.registros_extraidos}, Guardados: {self.registros_guardados}"
            )

            self.db.add(metricas)
            self.db.commit()

            logger.info("📈 Métricas guardadas")

        except Exception as e:
            logger.error(f"❌ Error guardando métricas: {e}")

    def ejecutar(self):
        try:
            logger.info("🚀 Iniciando ETL de Anime...")

            for page in range(1, 3):
                animes = self.extraer_animes(page)

                for anime in animes:
                    datos = self.procesar_anime(anime)
                    if datos:
                        self.guardar_en_bd(datos)

                time.sleep(1)

            estado = "SUCCESS" if self.registros_fallidos == 0 else "PARTIAL"
            self.guardar_metricas(estado)

            return True

        except Exception as e:
            logger.error(f"❌ Error general: {e}")
            self.guardar_metricas("FAILED")
            return False

        finally:
            self.db.close()

    def mostrar_resumen(self):
        print("\n" + "="*50)
        print("RESUMEN ETL - ANIME")
        print("="*50)
        print(f"Extraídos: {self.registros_extraidos}")
        print(f"Guardados: {self.registros_guardados}")
        print(f"Fallidos: {self.registros_fallidos}")
        print("="*50 + "\n")


if __name__ == "__main__":
    etl = JikanETL()
    exito = etl.ejecutar()
    etl.mostrar_resumen()

    exit(0 if exito else 1)