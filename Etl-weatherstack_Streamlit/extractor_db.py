import pandas as pd
import time
import logging
from dotenv import load_dotenv

from scripts.database import SessionLocal
from scripts.models import Ciudad, RegistroClima, MetricasETL

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherstackETL:
    def __init__(self):
        self.db = SessionLocal()
        self.tiempo_inicio = time.time()
        self.registros_guardados = 0
        self.registros_fallidos = 0

    def _obtener_ciudad(self, nombre):
        ciudad = self.db.query(Ciudad).filter(Ciudad.nombre == nombre).first()

        if not ciudad:
            ciudad = Ciudad(nombre=nombre, pais="Colombia")
            self.db.add(ciudad)
            self.db.commit()
            self.db.refresh(ciudad)
            logger.info(f"🏙️ Ciudad registrada: {nombre}")

        return ciudad

    def cargar_desde_csv(self):
        df = pd.read_csv("data_clima_limpio.csv")
        logger.info(f"📊 {len(df)} registros a procesar")

        for _, row in df.iterrows():
            try:
                ciudad = self._obtener_ciudad(row["ciudad"])

                registro = RegistroClima(
                    ciudad_id=ciudad.id,
                    temperatura=row["temperatura"],
                    humedad=row["humedad"],
                    velocidad_viento=row["velocidad_viento"],
                    descripcion=row["descripcion"]
                )

                self.db.add(registro)
                self.registros_guardados += 1

            except Exception as e:
                logger.error(f"Error: {str(e)}")
                self.registros_fallidos += 1

        self.db.commit()

    def guardar_metricas(self, estado):
        tiempo = time.time() - self.tiempo_inicio

        metricas = MetricasETL(
            registros_extraidos=0,
            registros_guardados=self.registros_guardados,
            registros_fallidos=self.registros_fallidos,
            tiempo_ejecucion_segundos=tiempo,
            estado=estado,
            mensaje=f"Guardados: {self.registros_guardados}"
        )

        self.db.add(metricas)
        self.db.commit()

    def ejecutar(self):
        try:
            logger.info("🚀 Cargando datos desde CSV...")

            self.cargar_desde_csv()

            estado = "SUCCESS"
            self.guardar_metricas(estado)

        except Exception as e:
            logger.error(str(e))
            self.guardar_metricas("FAILED")

        finally:
            self.db.close()


if __name__ == "__main__":
    etl = WeatherstackETL()
    etl.ejecutar()