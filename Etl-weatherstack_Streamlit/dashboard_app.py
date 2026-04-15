#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Clima ETL",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🌍 Dashboard de Clima - ETL Weatherstack")
st.markdown("---")

# Datos de ejemplo
data = {
    "Ciudad": ["Bogotá", "Medellín", "Cali", "Barranquilla"],
    "Temperatura": [18, 26, 28, 30],
    "Sensación Térmica": [17, 27, 29, 32],
    "Humedad": [75, 65, 70, 80],
    "Viento": [10, 8, 12, 15],
    "Descripción": ["Nublado", "Soleado", "Parcialmente nublado", "Soleado"]
}

df = pd.DataFrame(data)

# Sidebar con filtros
st.sidebar.title("🔧 Filtros")

ciudades_filtro = st.sidebar.multiselect(
    "Selecciona Ciudades:",
    options=df['Ciudad'].unique(),
    default=df['Ciudad'].unique()
)

df_filtrado = df[df['Ciudad'].isin(ciudades_filtro)]

# Métricas principales
st.subheader("📈 Métricas Principales")
col1, col2, col3, col4 = st.columns(4)

with col1:
    temp_promedio = df_filtrado['Temperatura'].mean()
    st.metric("🌡️ Temp. Promedio", f"{temp_promedio:.1f}°C")

with col2:
    humedad_promedio = df_filtrado['Humedad'].mean()
    st.metric("💧 Humedad Promedio", f"{humedad_promedio:.1f}%")

with col3:
    viento_maximo = df_filtrado['Viento'].max()
    st.metric("💨 Viento Máximo", f"{viento_maximo} km/h")

with col4:
    total_registros = len(df_filtrado)
    st.metric("📊 Total Registros", total_registros)

st.markdown("---")

# Visualizaciones
st.subheader("📉 Visualizaciones")

col1, col2 = st.columns(2)

with col1:
    fig_temp = px.bar(
        df_filtrado,
        x="Ciudad",
        y="Temperatura",
        title="Temperatura por Ciudad",
        color="Temperatura"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    fig_hum = px.bar(
        df_filtrado,
        x="Ciudad",
        y="Humedad",
        title="Humedad por Ciudad",
        color="Humedad"
    )
    st.plotly_chart(fig_hum, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    fig_scatter = px.scatter(
        df_filtrado,
        x="Temperatura",
        y="Humedad",
        size="Viento",
        color="Ciudad",
        title="Temperatura vs Humedad"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    fig_viento = px.bar(
        df_filtrado,
        x="Ciudad",
        y="Viento",
        title="Velocidad del Viento",
        color="Viento"
    )
    st.plotly_chart(fig_viento, use_container_width=True)

st.markdown("---")

st.subheader("📋 Datos")
st.dataframe(df_filtrado, use_container_width=True)