import streamlit as st
import plotly.express as px
import pandas as pd
import os

# 1. Configuración de página
st.set_page_config(page_title="Dashboard General", page_icon="📊", layout="wide")

# 2. CSS para mantener el estilo oscuro y profesional
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; }
    h1, h2, h3 { color: #ffffff !important; }
    .stPlotlyChart { background-color: #1e1e26; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. Bloque de Seguridad: Carga automática de datos
if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ No se encontró el dataset. Asegúrate de que existe en la carpeta /datasets/")
        st.stop()

df_estres = st.session_state.datasets['estres']

# 4. Interfaz del Dashboard
st.title("📊 Dashboard General de Datos Estudiantiles")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Niveles de Estrés")
    fig_estres = px.histogram(
        df_estres, x="stress_level", nbins=3, color="stress_level",
        template="plotly_dark"
    )
    st.plotly_chart(fig_estres, use_container_width=True)

with col2:
    st.subheader("Relación: Sueño vs Rendimiento")
    fig_scatter = px.scatter(
        df_estres, x="sleep_quality", y="academic_performance", 
        color="stress_level", template="plotly_dark"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

st.subheader("Análisis de Factores de Riesgo")
col3, col4 = st.columns(2)

with col3:
    st.write("Promedio de Ansiedad según Nivel de Estrés")
    df_promedio = df_estres.groupby('stress_level')['anxiety_level'].mean().reset_index()
    fig_bar = px.bar(df_promedio, x='stress_level', y='anxiety_level', color='stress_level', template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.write("Impacto de la Presión de Pares en el Estrés")
    fig_box = px.box(df_estres, x="stress_level", y="peer_pressure", color="stress_level", template="plotly_dark")
    st.plotly_chart(fig_box, use_container_width=True)
