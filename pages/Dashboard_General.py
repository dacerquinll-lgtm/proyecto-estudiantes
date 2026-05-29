import streamlit as st
import plotly.express as px
import pandas as pd
import os

# 1. Configuración de página
st.set_page_config(page_title="Analytics Central", layout="wide")

# 2. CSS profesional
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

# 3. Carga de datos
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

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df))
col2.metric("Estrés Promedio", mapa_label.get(int(round(df['stress_level'].mean())), "N/A"))
col3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

st.markdown("---")

tab1, tab2 = st.tabs(["📉 Rendimiento por Estrés", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("Impacto del Estrés en el Rendimiento Académico")
    
    # Agrupamos rendimiento por nivel de estrés
    df_rend = df.groupby(['stress_label'])['academic_performance'].mean().reset_index()
    orden = ["BAJO", "MODERADO", "ALTO"]
    df_rend['stress_label'] = pd.Categorical(df_rend['stress_label'], categories=orden, ordered=True)
    df_rend = df_rend.sort_values('stress_label')
    
    fig1 = px.bar(df_rend, x="stress_label", y="academic_performance", 
                  color="stress_label", template="plotly_dark",
                  color_discrete_map=colores_niveles,
                  labels={"stress_label": "Nivel de Estrés", 
                          "academic_performance": "Promedio de Rendimiento"})
    
    fig1.update_yaxes(range=[0, 5])
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_box = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    fig2 = px.bar(df_box, x='stress_label', y='anxiety_level', 
                  color='stress_label', template="plotly_dark",
                  color_discrete_map=colores_niveles)
    st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Interpretación:** Este gráfico demuestra claramente que a medida que aumenta el nivel de estrés, el rendimiento académico tiende a disminuir.")
