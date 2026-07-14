import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# Dashboard es la página 2
pagina_activa = 2

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
    .header-institucional {
        background-color: #0c1c30;
        padding: 20px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        margin-top: 0px !important;
        margin-bottom: 0px;
        border-radius: 8px 8px 0 0;
    }
    .header-institucional h2 { color: white !important; margin: 0; font-size: 1.2rem !important; font-weight: 600 !important; }
    
    /* Menú Oficial (Azul diferenciado #1a2a40) */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        background-color: #1a2a40 !important;
        padding: 10px 20px !important;
        margin-top: 0px !important;
        margin-bottom: 30px !important;
        border-radius: 0 0 8px 8px !important;
        gap: 0px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="stPageLink"] a {
        background-color: transparent !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 0.9rem !important;
        padding: 6px 12px !important;
        text-decoration: none !important;
        display: inline-flex !important;
    }
    
    /* Resaltado de página activa (Dashboard = 2da columna) */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) > div[data-testid="column"]:nth-of-type(2) div[data-testid="stPageLink"] a {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 4px !important;
    }
    
    h1, h2, h3, h4 { color: #0c1c30 !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color: #0c1c30 !important; }
    div[data-testid="stMetric"] { padding: 15px !important; border-radius: 8px !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08) !important; }
    
    div[data-testid="column"]:has(div[data-testid="stMetric"]):nth-of-type(1) div[data-testid="stMetric"] { background-color: #e3f2fd !important; border: 1px solid #90caf9 !important; }
    div[data-testid="column"]:has(div[data-testid="stMetric"]):nth-of-type(2) div[data-testid="stMetric"] { background-color: #fff3e0 !important; border: 1px solid #ffcc80 !important; }
    div[data-testid="column"]:has(div[data-testid="stMetric"]):nth-of-type(3) div[data-testid="stMetric"] { background-color: #ffebee !important; border: 1px solid #ffcdd2 !important; }
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
""", unsafe_allow_html=True)

# Menú Oficial
cols_nav = st.columns([0.8, 1.2, 1.2, 1.4, 1.4])
with cols_nav[0]: st.page_link("app.py", label="Inicio")
with cols_nav[1]: st.page_link("pages/Dashboard_General.py", label="Dashboard General")
with cols_nav[2]: st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés")
with cols_nav[3]: st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación")
with cols_nav[4]: st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios")

if 'datasets' not in st.session_state or st.session_state['datasets'] is None:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ Archivo no encontrado.")
        st.stop()

df = st.session_state.datasets['estres']
mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
df['stress_label'] = df['stress_level'].map(mapa_label)

st.title("📊 Centro de Analítica Estudiantil")

col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df))
col2.metric("Nivel de Estrés Promedio", mapa_label.get(int(round(df['stress_level'].mean())), "N/A"))
col3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

tab1, tab2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    df_line = df.groupby(['stress_level', 'stress_label'])['academic_performance'].mean().reset_index().sort_values('stress_level')
    fig1 = px.line(df_line, x="stress_label", y="academic_performance", markers=True, template="plotly_white")
    fig1.update_layout(font=dict(color="#0c1c30", size=14))
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', color='stress_label', template="plotly_white")
    fig2.update_layout(showlegend=False, font=dict(color="#0c1c30", size=14))
    st.plotly_chart(fig2, use_container_width=True)
