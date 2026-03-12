#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Anime ETL",
    page_icon="🎌",
    layout="wide"
)

st.title("🎌 Dashboard de Anime - Jikan API")
st.markdown("---")

# ==========================
# Cargar datos
# ==========================

df = pd.read_csv("data/top_anime.csv")

# Mostrar columnas (puedes quitar esto después)
# st.write(df.columns)

# ==========================
# Limpieza dinámica
# ==========================

columnas_numericas = []

for col in ["score", "episodes", "popularity"]:
    if col in df.columns:
        columnas_numericas.append(col)

if columnas_numericas:
    df = df.dropna(subset=columnas_numericas)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("🔎 Filtros")

if "score" in df.columns:
    score_min = st.sidebar.slider(
        "Score mínimo:",
        float(df["score"].min()),
        float(df["score"].max()),
        float(df["score"].min())
    )
    df = df[df["score"] >= score_min]

if "episodes" in df.columns:
    episodios_min = st.sidebar.slider(
        "Episodios mínimos:",
        int(df["episodes"].min()),
        int(df["episodes"].max()),
        int(df["episodes"].min())
    )
    df = df[df["episodes"] >= episodios_min]

# ==========================
# MÉTRICAS
# ==========================

st.subheader("📈 Métricas Principales")

col1, col2, col3 = st.columns(3)

if "score" in df.columns:
    col1.metric("⭐ Score Promedio", f"{df['score'].mean():.2f}")

if "episodes" in df.columns:
    col2.metric("📺 Episodios Promedio", f"{df['episodes'].mean():.1f}")

if "popularity" in df.columns:
    col3.metric("🔥 Popularidad Promedio", f"{df['popularity'].mean():.0f}")

st.markdown("---")

# ==========================
# VISUALIZACIONES
# ==========================

st.subheader("📊 Visualizaciones")

if "score" in df.columns:
    fig_score = px.bar(
        df.sort_values("score", ascending=False).head(10),
        x="title",
        y="score",
        title="Top 10 Anime por Score"
    )
    st.plotly_chart(fig_score, use_container_width=True)

if "popularity" in df.columns:
    fig_pop = px.bar(
        df.sort_values("popularity").head(10),
        x="title",
        y="popularity",
        title="Top 10 Más Populares"
    )
    st.plotly_chart(fig_pop, use_container_width=True)

if all(col in df.columns for col in ["score", "episodes"]):
    fig_scatter = px.scatter(
        df,
        x="episodes",
        y="score",
        hover_name="title",
        title="Relación Episodios vs Score"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ==========================
# TABLA
# ==========================

st.subheader("📋 Datos Detallados")
st.dataframe(df, use_container_width=True, height=400)