import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.session_state['datasets'] = None

st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    [data-testid="stHeader"] {
        background: transparent;
        height: 0px;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0c1c30 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] {
        background-color: #0c1c30 !important;
    }
    .header-institucional {
        background-color: #0c1c30;
        padding: 15px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        border-radius: 8px;
        margin-bottom: 30px;
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
    .bienvenida-titulo {
        color: #2e7d32 !important;
        font-size: 2.2rem !important;
        font-weight: bold !important;
        margin-bottom: 5px;
    }
    .bienvenida-sub {
        color: #0c1c30 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        line-height: 1.2;
        margin-bottom: 20px;
    }
    .bienvenida-texto {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 30px;
    }
    .btn-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        max-width: 320px;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease;
        text-align: center;
    }
    div.stButton > button[key="btn_eval"] {
        background-color: #1b5e20 !important;
        color: white !important;
        border: none !important;
    }
    div.stButton > button[key="btn_eval"]:hover {
        background-color: #2e7d32 !important;
        transform: translateY(-2px);
    }
    div.stButton > button[key="btn_info"] {
        background-color: transparent !important;
        color: #1b5e20 !important;
        border: 2px solid #1b5e20 !important;
    }
    div.stButton > button[key="btn_info"]:hover {
        background-color: #e8f5e9 !important;
        transform: translateY(-2px);
    }
    .status-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .status-card h4 {
        color: #0c1c30 !important;
        margin-bottom: 15px;
    }
    .illustration-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        margin-top: 20px;
    }
    .illustration-box img {
        max-width: 85%;
        height: auto;
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
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    st.markdown("""
        <div class="home-container">
            <h3 class="bienvenida-titulo">Bienvenido</h3>
            <h1 class="bienvenida-sub">Sistema Inteligente para la Reducción de Estrés Académico</h1>
            <p class="bienvenida-texto">
                Plataforma basada en modelos de Machine Learning que analiza tus hábitos académicos 
                y personales para identificar tu nivel de estrés y brindarte recomendaciones personalizadas.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="btn-container">', unsafe_allow_html=True)
    st.button("Iniciar evaluación ➔", key="btn_eval")
    st.button("Ver información ⓘ", key="btn_info")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.markdown("<h4>Estado del Sistema</h4>", unsafe_allow_html=True)
    
    if st.session_state['datasets'] is not None:
        st.success("✅ **Conexión con el Modelo:** RF-Optimizado v2.4")
        st.info("✅ **Estado de Datos:** Dataset cargado correctamente.")
    else:
        st.error("⚠️ Error crítico: No se encontró 'datasets/StressLevelDataset_limpio.csv'")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="illustration-box">
            <img src="https://img.freepik.com/vectores-gratis/concept-concept-de-sante-mentale-illustration_114360-8452.jpg">
        </div>
    """, unsafe_allow_html=True)
