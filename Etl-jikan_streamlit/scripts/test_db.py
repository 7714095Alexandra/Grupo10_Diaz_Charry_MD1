#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from scripts.database import test_connection, engine
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("PRUEBA DE CONEXIÓN A POSTGRESQL (JIKAN)")
    print("="*50)
    
    if test_connection():
        print("✅ Conexión exitosa a la base de datos")
        print(f"Base de datos: {engine.url.database}")
        print(f"Host: {engine.url.host}")
        print(f"Puerto: {engine.url.port}")
        print(f"Usuario: {engine.url.username}")
    else:
        print("❌ No se pudo conectar a la base de datos")
        print("\nVerifica:")
        print("- PostgreSQL está corriendo")
        print("- Archivo .env está bien configurado")
        print("- Base de datos 'jikan_etl' existe")
        print("- Usuario y contraseña son correctos")
    
    print("="*50 + "\n")