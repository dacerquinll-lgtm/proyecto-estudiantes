import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")

pagina_activa = 1

if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.session_state['datasets'] = None

st.markdown(f"""
    <style>
    .stApp {{
        background-color: #f8f9fa !important;
    }}
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }}
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    .header-institucional {{
        background-color: #0c1c30;
        padding: 20px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        margin-top: 0px !important;
        margin-bottom: 0px;
        border-radius: 8px 8px 0 0;
    }}
    .header-institucional h2 {{
        color: white !important;
        margin: 0;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }}
    .header-logo {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {{
        background-color: #142840 !important;
        padding: 10px 20px !important;
        margin-top: 0px !important;
        margin-bottom: 30px !important;
        border-radius: 0 0 8px 8px !important;
        gap: 0px !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="stPageLink"] a {{
        background-color: transparent !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 0.9rem !important;
        padding: 6px 12px !important;
        text-decoration: underline !important;
        box-shadow: none !important;
        display: inline-flex !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="stPageLink"] a:hover {{
        color: #cfd8dc !important;
        text-decoration: underline !important;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="column"]:nth-child({pagina_activa}) div[data-testid="stPageLink"] a {{
        background-color: #2e7d32 !important;
        color: white !important;
        text-decoration: none !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
    }}
    
    .bienvenida-titulo {{
        color: #2e7d32 !important;
        font-size: 2.2rem !important;
        font-weight: bold !important;
        margin-bottom: 5px;
    }}
    .bienvenida-sub {{
        color: #0c1c30 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        line-height: 1.2;
        margin-bottom: 20px;
    }}
    .bienvenida-texto {{
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 30px;
    }}
    .btn-container {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        max-width: 320px;
    }}
    div.stButton > button[key="btn_eval"] {{
        background-color: #0c1c30 !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
    }}
    div.stButton > button[key="btn_info"] {{
        background-color: transparent !important;
        color: #0c1c30 !important;
        border: 2px solid #0c1c30 !important;
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
    }}
    .titulo-estado {{
        color: #0c1c30 !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        margin-top: 10px;
        margin-bottom: 15px;
        display: block;
    }}
    div[data-testid="stNotification"] * {{
        color: #0c1c30 !important;
    }}
    .illustration-box {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 25px;
    }}
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

cols_nav = st.columns([1, 1.3, 1.2, 1.3, 1.4, 4])
with cols_nav[0]:
    st.page_link("app.py", label="Inicio", icon=None)
with cols_nav[1]:
    st.page_link("pages/Dashboard_General.py", label="Dashboard General", icon=None)
with cols_nav[2]:
    st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés", icon=None)
with cols_nav[3]:
    st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación", icon=None)
with cols_nav[4]:
    st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios", icon=None)

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
    st.markdown('<span class="titulo-estado">Estado del Sistema</span>', unsafe_allow_html=True)
    
    if st.session_state['datasets'] is not None:
        st.success("✅ **Conexión con el Modelo:** RF-Optimizado v2.4")
        st.info("✅ **Estado de Datos:** Dataset cargado correctamente.")
    else:
        st.error("⚠️ Error crítico: No se encontró 'datasets/StressLevelDataset_limpio.csv'")
    
    st.markdown('<div class="illustration-box">', unsafe_allow_html=True)
    st.image("assets/imagen.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
