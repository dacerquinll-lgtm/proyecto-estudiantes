import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="Analytics Central", layout="wide")

# CSS para estilo profesional
st.markdown("<style>.stApp { background-color: #0f1116; } h1, h2, h3 { color: #ffffff !important; }</style>", unsafe_allow_html=True)

# Carga de datos
if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("Archivo no encontrado.")
        st.stop()

df = st.session_state.datasets['estres']

# Título y KPIs
st.title("📊 Centro de Analítica Estudiantil")
col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df))
col2.metric("Nivel de Estrés Promedio", round(df['stress_level'].mean(), 2))
col3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

st.markdown("---")

# Gráficos Unificados con TABS para no saturar la vista
tab1, tab2 = st.tabs(["📉 Análisis de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("Calidad de Sueño vs Rendimiento")
    fig = px.scatter(df, x="sleep_quality", y="academic_performance", 
                     color="stress_level", template="plotly_dark", trendline="ols")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_box = df.groupby('stress_level')['anxiety_level'].mean().reset_index()
    fig2 = px.bar(df_box, x='stress_level', y='anxiety_level', 
                  color='stress_level', template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Interpretación:** Los gráficos muestran cómo variables críticas afectan el rendimiento y la salud mental.")
