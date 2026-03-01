#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Avanzado Anime",
    page_icon="🎌",
    layout="wide"
)

st.title("🎌 Dashboard Avanzado - Análisis de Anime (Jikan API)")
st.markdown("---")

# ==========================
# CARGAR DATOS
# ==========================

df = pd.read_csv("data/top_anime.csv")

# Limpiar valores nulos si existen columnas
columnas_numericas = [col for col in ["score", "episodes", "popularity"] if col in df.columns]
if columnas_numericas:
    df = df.dropna(subset=columnas_numericas)

# ==========================
# PESTAÑAS
# ==========================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Vista General",
    "📈 Análisis por Score",
    "🔍 Análisis Estadístico",
    "📋 Datos Detallados"
])

# ======================================================
# 📊 TAB 1 - VISTA GENERAL
# ======================================================

with tab1:
    st.subheader("Resumen General")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎬 Total Animes", len(df))

    if "score" in df.columns:
        with col2:
            st.metric("⭐ Score Promedio", f"{df['score'].mean():.2f}")

    if "episodes" in df.columns:
        with col3:
            st.metric("📺 Episodios Promedio", f"{df['episodes'].mean():.1f}")

    st.markdown("---")

    if "score" in df.columns:
        fig = px.bar(
            df.sort_values("score", ascending=False).head(10),
            x="title",
            y="score",
            title="Top 10 Anime por Score",
            color="score"
        )
        st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 📈 TAB 2 - ANÁLISIS POR SCORE
# ======================================================

with tab2:
    st.subheader("Distribución de Score")

    if "score" in df.columns:
        fig = px.histogram(
            df,
            x="score",
            nbins=20,
            title="Distribución de Calificaciones"
        )
        st.plotly_chart(fig, use_container_width=True)

        if "popularity" in df.columns:
            fig2 = px.scatter(
                df,
                x="popularity",
                y="score",
                size="episodes" if "episodes" in df.columns else None,
                hover_name="title",
                title="Relación Popularidad vs Score"
            )
            st.plotly_chart(fig2, use_container_width=True)

# ======================================================
# 🔍 TAB 3 - ANÁLISIS ESTADÍSTICO
# ======================================================

with tab3:
    st.subheader("Estadísticas Generales")

    st.write("📊 Estadísticas Descriptivas:")
    st.dataframe(df.describe(), use_container_width=True)

    if "episodes" in df.columns:
        fig = px.box(
            df,
            y="episodes",
            title="Distribución de Episodios"
        )
        st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 📋 TAB 4 - DATOS DETALLADOS
# ======================================================

with tab4:
    st.subheader("Tabla Completa de Animes")

    filtro_nombre = st.text_input("Buscar por nombre:")

    if filtro_nombre:
        df_filtrado = df[df["title"].str.contains(filtro_nombre, case=False)]
    else:
        df_filtrado = df

    st.dataframe(df_filtrado, use_container_width=True, height=500)