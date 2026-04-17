#!/usr/bin/env python3
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from scripts.database import Base


class Anime(Base):
    __tablename__ = "anime"
    __table_args__ = {"schema": "public"}  # 👈 importante para Supabase

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Datos principales
    titulo = Column(String(255), nullable=False)
    tipo = Column(String(50))
    episodios = Column(Integer)

    # Métricas
    score = Column(Float)
    popularity = Column(Integer)
    miembros = Column(Integer)

    # Extra
    estado = Column(String(50))
    fecha_emision = Column(String(100))

    # Control ETL
    fecha_extraccion = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Anime(titulo='{self.titulo}', score={self.score})>"


class Genero(Base):
    __tablename__ = "generos"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Genero(nombre='{self.nombre}')>"


class AnimeGenero(Base):
    __tablename__ = "anime_generos"
    __table_args__ = {"schema": "public"}

    anime_id = Column(Integer, primary_key=True)
    genero_id = Column(Integer, primary_key=True)


class MetricasETL(Base):
    __tablename__ = "metricas_etl"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ejecucion = Column(DateTime, default=datetime.utcnow)

    registros_extraidos = Column(Integer, nullable=False)
    registros_guardados = Column(Integer, nullable=False)
    registros_fallidos = Column(Integer, default=0)

    tiempo_ejecucion_segundos = Column(Float, nullable=False)
    estado = Column(String(50), nullable=False)
    mensaje = Column(String(500))

    def __repr__(self):
        return f"<ETL(estado='{self.estado}', registros={self.registros_guardados})>"