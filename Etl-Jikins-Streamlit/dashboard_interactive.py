#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Interactivo Anime",
    page_icon="🎛️",
    layout="wide"
)

# ==========================
# CSS Personalizado
# ==========================

st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎛️ Dashboard Interactivo - Anime Jikan API")

# ==========================
# CARGAR DATOS
# ==========================

df = pd.read_csv("data/top_anime.csv")

# Limpiar nulos si existen columnas
columnas_numericas = [col for col in ["score", "episodes", "popularity"] if col in df.columns]
if columnas_numericas:
    df = df.dropna(subset=columnas_numericas)

# ==========================
# SIDEBAR CONTROLES
# ==========================

st.sidebar.markdown("### 🔧 Controles")

# Filtro por nombre
busqueda = st.sidebar.text_input("🔎 Buscar anime por nombre")

# Filtro por score
if "score" in df.columns:
    score_min, score_max = st.sidebar.slider(
        "⭐ Rango de Score",
        float(df["score"].min()),
        float(df["score"].max()),
        (float(df["score"].min()), float(df["score"].max()))
    )
else:
    score_min, score_max = None, None

# Filtro por episodios
if "episodes" in df.columns:
    ep_min, ep_max = st.sidebar.slider(
        "📺 Rango de Episodios",
        int(df["episodes"].min()),
        int(df["episodes"].max()),
        (int(df["episodes"].min()), int(df["episodes"].max()))
    )
else:
    ep_min, ep_max = None, None

# Aplicar filtros
df_filtrado = df.copy()

if busqueda:
    df_filtrado = df_filtrado[df_filtrado["title"].str.contains(busqueda, case=False)]

if score_min is not None:
    df_filtrado = df_filtrado[
        (df_filtrado["score"] >= score_min) &
        (df_filtrado["score"] <= score_max)
    ]

if ep_min is not None:
    df_filtrado = df_filtrado[
        (df_filtrado["episodes"] >= ep_min) &
        (df_filtrado["episodes"] <= ep_max)
    ]

# ==========================
# KPIs
# ==========================

if not df_filtrado.empty:

    st.markdown("### 📊 Indicadores Clave")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🎬 Total Animes", len(df_filtrado))

    if "score" in df.columns:
        with col2:
            st.metric("⭐ Score Promedio", f"{df_filtrado['score'].mean():.2f}")

    if "episodes" in df.columns:
        with col3:
            st.metric("📺 Episodios Promedio", f"{df_filtrado['episodes'].mean():.1f}")

    if "popularity" in df.columns:
        with col4:
            st.metric("🔥 Popularidad Promedio", f"{df_filtrado['popularity'].mean():.0f}")

    st.markdown("---")

    # ==========================
    # GRÁFICAS
    # ==========================

    col1, col2 = st.columns(2)

    # Boxplot Score
    if "score" in df.columns:
        with col1:
            st.markdown("#### Distribución de Score")
            fig = px.box(
                df_filtrado,
                y="score",
                points="all",
                title="Distribución de Calificaciones"
            )
            st.plotly_chart(fig, use_container_width=True)

    # Popularidad
    if "popularity" in df.columns:
        with col2:
            st.markdown("#### Popularidad por Anime")
            fig = px.bar(
                df_filtrado.sort_values("popularity").head(10),
                x="title",
                y="popularity",
                title="Top 10 Más Populares"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Scatter interactivo
    if all(col in df.columns for col in ["score", "episodes"]):
        st.markdown("#### 📈 Relación Episodios vs Score")

        fig = px.scatter(
            df_filtrado,
            x="episodes",
            y="score",
            size="popularity" if "popularity" in df.columns else None,
            hover_name="title",
            title="Relación Episodios y Score"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ==========================
    # TABLA INTERACTIVA
    # ==========================

    st.markdown("#### 📋 Datos Detallados")

    mostrar_todos = st.checkbox("Mostrar todos los registros", value=False)

    columnas_mostrar = st.multiselect(
        "Columnas a mostrar:",
        df_filtrado.columns.tolist(),
        default=df_filtrado.columns.tolist()
    )

    if mostrar_todos:
        st.dataframe(df_filtrado[columnas_mostrar], use_container_width=True, height=600)
    else:
        st.dataframe(df_filtrado[columnas_mostrar].head(20), use_container_width=True)

    # Descargar CSV
    st.markdown("---")

    csv = df_filtrado.to_csv(index=False)

    st.download_button(
        label="⬇️ Descargar datos filtrados",
        data=csv,
        file_name=f"anime_filtrado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados")