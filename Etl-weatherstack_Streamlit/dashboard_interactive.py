#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Dashboard Interactivo",
    page_icon="🎛️",
    layout="wide"
)

st.title("🎛️ Dashboard Interactivo - Control Total")

# ===============================
# DATOS SIMULADOS
# ===============================

ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla"]
paises = {
    "Bogotá": "Colombia",
    "Medellín": "Colombia",
    "Cali": "Colombia",
    "Barranquilla": "Colombia"
}

data = []

for i in range(100):
    ciudad = random.choice(ciudades)
    data.append({
        "Ciudad": ciudad,
        "País": paises[ciudad],
        "Temperatura": random.uniform(18, 35),
        "Sensación": random.uniform(18, 36),
        "Humedad": random.uniform(60, 90),
        "Viento": random.uniform(5, 20),
        "Descripción": random.choice(["Soleado", "Nublado", "Lluvia"]),
        "Fecha": datetime.now() - timedelta(days=random.randint(0, 30))
    })

df = pd.DataFrame(data)

# ===============================
# SIDEBAR
# ===============================

st.sidebar.markdown("### 🔧 Controles")

ciudades_seleccionadas = st.sidebar.multiselect(
    "🏙️ Ciudades a Mostrar",
    options=ciudades,
    default=ciudades[:2]
)

col1, col2 = st.sidebar.columns(2)

with col1:
    fecha_inicio = st.sidebar.date_input(
        "📅 Desde:",
        value=datetime.now() - timedelta(days=30)
    )

with col2:
    fecha_fin = st.sidebar.date_input(
        "📅 Hasta:",
        value=datetime.now()
    )

col1, col2 = st.sidebar.columns(2)

with col1:
    temp_min = st.sidebar.slider("🌡️ Temp Mín (°C):", -50, 50, value=-10)

with col2:
    temp_max = st.sidebar.slider("🌡️ Temp Máx (°C):", -50, 50, value=40)

# ===============================
# FILTROS
# ===============================

df_filtrado = df[
    (df["Ciudad"].isin(ciudades_seleccionadas)) &
    (df["Fecha"] >= pd.to_datetime(fecha_inicio)) &
    (df["Fecha"] <= pd.to_datetime(fecha_fin)) &
    (df["Temperatura"] >= temp_min) &
    (df["Temperatura"] <= temp_max)
]

# ===============================
# DASHBOARD
# ===============================

if not df_filtrado.empty:

    st.markdown("### 📊 Indicadores Clave")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🌡️ Temp Max", f"{df_filtrado['Temperatura'].max():.1f}°C")

    with col2:
        st.metric("🌡️ Temp Min", f"{df_filtrado['Temperatura'].min():.1f}°C")

    with col3:
        st.metric("🌡️ Temp Prom", f"{df_filtrado['Temperatura'].mean():.1f}°C")

    with col4:
        st.metric("💧 Humedad Prom", f"{df_filtrado['Humedad'].mean():.1f}%")

    with col5:
        st.metric("💨 Viento Max", f"{df_filtrado['Viento'].max():.1f} km/h")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Comparativa de Temperaturas")

        fig = px.box(
            df_filtrado,
            x="Ciudad",
            y="Temperatura",
            color="Ciudad",
            title="Distribución de Temperaturas por Ciudad"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.markdown("#### Promedio de Humedad")

        humedad_ciudad = df_filtrado.groupby("Ciudad")["Humedad"].mean().reset_index()

        fig = px.bar(
            humedad_ciudad,
            x="Ciudad",
            y="Humedad",
            color="Humedad",
            color_continuous_scale="Blues"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.markdown("#### 📈 Evolución Temporal")

    temp_tiempo = df_filtrado.groupby(["Fecha", "Ciudad"])["Temperatura"].mean().reset_index()

    fig = px.line(
        temp_tiempo,
        x="Fecha",
        y="Temperatura",
        color="Ciudad",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.markdown("#### 📋 Datos Detallados")

    col1, col2 = st.columns(2)

    with col1:
        mostrar_todos = st.checkbox("Mostrar todos los registros", value=False)

    with col2:
        columnas_mostrar = st.multiselect(
            "Columnas a mostrar:",
            df_filtrado.columns.tolist(),
            default=["Ciudad", "Temperatura", "Humedad", "Descripción", "Fecha"]
        )

    if mostrar_todos:
        st.dataframe(df_filtrado[columnas_mostrar], use_container_width=True, height=600)
    else:
        st.dataframe(df_filtrado[columnas_mostrar].head(20), use_container_width=True)

    st.markdown("---")

    csv = df_filtrado.to_csv(index=False)

    st.download_button(
        label="⬇️ Descargar datos como CSV",
        data=csv,
        file_name=f"clima_datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:

    st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados")