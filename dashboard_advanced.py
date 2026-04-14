#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Dashboard Avanzado clima",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌍 Dashboard Avanzado - Análisis de Clima")
st.markdown("---")

# ==============================
# DATOS SIMULADOS
# ==============================

ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla"]

data = []

for i in range(30):
    for ciudad in ciudades:
        data.append({
            "Fecha": datetime.now() - timedelta(days=random.randint(0,7)),
            "Ciudad": ciudad,
            "Temperatura": random.randint(18,32),
            "Humedad": random.randint(60,90),
            "Viento": random.randint(5,20),
            "Descripción": random.choice(["Soleado","Nublado","Lluvia"])
        })

df = pd.DataFrame(data)

# ==============================
# PESTAÑAS
# ==============================

tab1, tab2, tab3, tab4 = st.tabs(["📊 Vista General", "📈 Histórico", "🔍 Análisis", "📋 Métricas ETL"])

# ==============================
# TAB 1
# ==============================

with tab1:

    st.subheader("Datos Actuales")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏙️ Ciudades", df["Ciudad"].nunique())

    with col2:
        st.metric("📊 Registros Totales", len(df))

    with col3:
        st.metric("⏰ Última Actualización", datetime.now().strftime("%Y-%m-%d %H:%M"))

    st.markdown("---")

    df_actual = df.sort_values("Fecha").drop_duplicates("Ciudad", keep="last")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            df_actual,
            x="Ciudad",
            y="Temperatura",
            title="Temperatura Actual",
            color="Temperatura",
            color_continuous_scale="RdYlBu_r"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            df_actual,
            values="Humedad",
            names="Ciudad",
            title="Distribución de Humedad"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.dataframe(df_actual, use_container_width=True)

# ==============================
# TAB 2
# ==============================

with tab2:

    st.subheader("Análisis Histórico")

    col1, col2 = st.columns(2)

    with col1:
        fecha_inicio = st.date_input("Desde:", value=datetime.now() - timedelta(days=7))

    with col2:
        fecha_fin = st.date_input("Hasta:", value=datetime.now())

    df_historico = df[
        (df["Fecha"] >= pd.to_datetime(fecha_inicio)) &
        (df["Fecha"] <= pd.to_datetime(fecha_fin))
    ]

    if not df_historico.empty:

        fig = px.line(
            df_historico,
            x="Fecha",
            y="Temperatura",
            color="Ciudad",
            title="Temperatura en el Tiempo",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.dataframe(df_historico, use_container_width=True)

    else:
        st.warning("No hay datos en ese rango de fechas")

# ==============================
# TAB 3
# ==============================

with tab3:

    st.subheader("Análisis Estadístico")

    for ciudad in df["Ciudad"].unique():

        with st.expander(f"📍 {ciudad}"):

            df_ciudad = df[df["Ciudad"] == ciudad]

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("🌡️ Temp Prom.", f"{df_ciudad['Temperatura'].mean():.1f}°C")

            with col2:
                st.metric("💧 Humedad Prom.", f"{df_ciudad['Humedad'].mean():.1f}%")

            with col3:
                st.metric("💨 Viento Prom.", f"{df_ciudad['Viento'].mean():.1f} km/h")

            with col4:
                st.metric("📊 Registros", len(df_ciudad))

# ==============================
# TAB 4
# ==============================

with tab4:

    st.subheader("Métricas de Ejecución ETL")

    data_metricas = []

    for i in range(10):

        data_metricas.append({
            "Fecha": datetime.now() - timedelta(days=i),
            "Estado": random.choice(["OK", "ERROR"]),
            "Extraídos": random.randint(10,50),
            "Guardados": random.randint(10,50),
            "Fallidos": random.randint(0,5),
            "Tiempo (s)": random.uniform(0.5,5)
        })

    df_metricas = pd.DataFrame(data_metricas)

    st.dataframe(df_metricas, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            df_metricas,
            x="Fecha",
            y="Guardados",
            color="Estado",
            title="Registros Guardados por Ejecución"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.scatter(
            df_metricas,
            x="Fecha",
            y="Tiempo (s)",
            size="Guardados",
            color="Estado",
            title="Duración de Ejecuciones"
        )

        st.plotly_chart(fig, use_container_width=True)