import streamlit as st
import plotly.express as px
import pandas as pd
import os

# Configuración de página
st.set_page_config(page_title="Analytics Central", layout="wide")

# CSS profesional
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; }
    h1, h2, h3 { color: #ffffff !important; }
    .stPlotlyChart { background-color: #1e1e26; border-radius: 15px; }
    .guia-box { 
        background-color: #262730; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #ffffff; margin-bottom: 20px; 
    }
    </style>
""", unsafe_allow_html=True)

# Carga de datos
if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ Archivo no encontrado.")
        st.stop()

df = st.session_state.datasets['estres']

# Mapeo de niveles
mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
colores_niveles = {"BAJO": "#00cc96", "MODERADO": "#ffa15a", "ALTO": "#ef553b"}
df['stress_label'] = df['stress_level'].map(mapa_label)

st.title("📊 Centro de Analítica Estudiantil")

# Guía
st.markdown("""
<div class="guia-box">
    <strong>Guía de Clasificación:</strong> 
    <span style="color: #00cc96;">● BAJO</span> | 
    <span style="color: #ffa15a;">● MODERADO</span> | 
    <span style="color: #ef553b;">● ALTO</span>
</div>
""", unsafe_allow_html=True)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df))
col2.metric("Estrés Promedio", mapa_label.get(int(round(df['stress_level'].mean())), "N/A"))
col3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

st.markdown("---")

tab1, tab2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("¿Cómo mejora tu rendimiento al dormir mejor?")
    # Agrupamos datos para una línea clara
    df_line = df.groupby(['sleep_quality', 'stress_label'])['academic_performance'].mean().reset_index()
    
    fig1 = px.line(df_line, x="sleep_quality", y="academic_performance", 
                   color="stress_label", markers=True,
                   template="plotly_dark", color_discrete_map=colores_niveles,
                   labels={"sleep_quality": "Calidad de Sueño (0-5)", 
                           "academic_performance": "Promedio de Rendimiento"})
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', 
                  color='stress_label', template="plotly_dark",
                  color_discrete_map=colores_niveles)
    st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Interpretación:** Observa cómo las líneas suben: ¡dormir mejor está directamente relacionado con mejores notas!")
