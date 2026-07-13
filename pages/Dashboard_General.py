import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    [data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .header-institucional {
        background-color: #0c1c30;
        padding: 15px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        border-radius: 8px 8px 0 0;
        margin-bottom: 0px;
    }
    .header-institucional h2 {
        color: white !important;
        margin: 0;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    .header-logo {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-bar {
        background-color: #142840;
        padding: 10px 20px;
        display: flex;
        gap: 15px;
        border-radius: 0 0 8px 8px;
        margin-bottom: 30px;
    }
    .nav-link {
        color: #cfd8dc !important;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        padding: 6px 12px;
        border-radius: 4px;
        transition: background 0.2s;
    }
    .nav-link:hover {
        background-color: #1c3b5e;
        color: #ffffff !important;
    }
    .nav-active {
        background-color: #2e7d32;
        color: white !important;
    }
    h1, h2, h3, h4 {
        color: #0c1c30 !important;
        font-weight: bold !important;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="metric-container"] * {
        color: #0c1c30 !important;
    }
    div[data-testid="stNotification"] * {
        color: #0c1c30 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-institucional">
        <div class="header-logo">
            <span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span>
        </div>
        <div>
            <h2>Sistema Inteligente para la Reducción de Estrés en Universitarios</h2>
        </div>
    </div>
    <div class="nav-bar">
        <a class="nav-link" href="/" target="_self">Inicio</a>
        <a class="nav-link nav-active" href="/Dashboard_General" target="_self">Dashboard General</a>
        <a class="nav-link" href="/Detector_de_Estres" target="_self">Detector de Estrés</a>
        <a class="nav-link" href="/Reportes_y_Exportacion" target="_self">Reportes y Exportación</a>
        <a class="nav-link" href="/Simulador_de_Escenarios" target="_self">Simulador de Escenarios</a>
    </div>
""", unsafe_allow_html=True)

if 'datasets' not in st.session_state or st.session_state['datasets'] is None:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ Archivo no encontrado. Por favor, asegúrese de tener 'datasets/StressLevelDataset_limpio.csv'.")
        st.stop()

df = st.session_state.datasets['estres']

mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
df['stress_label'] = df['stress_level'].map(mapa_label)

st.title("📊 Centro de Analítica Estudiantil")

col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df))
col2.metric("Nivel de Estrés Promedio", mapa_label.get(int(round(df['stress_level'].mean())), "N/A"))
col3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("Evolución del Rendimiento Académico")
    
    df_line = df.groupby(['stress_level', 'stress_label'])['academic_performance'].mean().reset_index()
    df_line = df_line.sort_values('stress_level')
    
    fig1 = px.line(df_line, x="stress_label", y="academic_performance", 
                   markers=True,
                   template="plotly_white",
                   line_shape="spline",
                   labels={"stress_label": "Nivel de Estrés", 
                           "academic_performance": "Rendimiento Académico Promedio"})
    
    fig1.update_traces(line_color="#0c1c30", line_width=4, marker=dict(size=12, color="#2e7d32"))
    fig1.update_yaxes(range=[0, 5])
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', 
                  color='stress_label', template="plotly_white",
                  labels={"stress_label": "Nivel de Estrés", 
                          "anxiety_level": "Nivel de Ansiedad Promedio"},
                  color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Interpretación:** La tendencia descendente confirma que, al aumentar el nivel de estrés, el rendimiento académico disminuye de forma consistente.")
