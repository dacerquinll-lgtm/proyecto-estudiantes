import streamlit as st
import pandas as pd
import os

# 1. Configuración de página (siempre al inicio)
st.set_page_config(page_title="MindCare Analytics", page_icon="🧠", layout="wide")

# 2. Inicialización del Dataset (Global)
if 'datasets' not in st.session_state:
    ruta = "datasets/data_estres.csv"
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.session_state['datasets'] = None # Indicador de error si no existe

# 3. CSS Avanzado (Estilo Dark Profesional)
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; }
    .metric-card {
        background: linear-gradient(135deg, #1e1e26 0%, #252530 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #333;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        color: white;
    }
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }
    .stInfo { background-color: #1e1e26; border-left: 5px solid #00d4ff; }
    div.stButton > button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        border: none;
        color: white;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

# 4. Interfaz Principal
st.title("🧠 MindCare Analytics")
st.subheader("Sistema Inteligente de Bienestar Estudiantil")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("""
    <div class="metric-card">
        <h3>Bienvenido de nuevo</h3>
        <p>Tu sistema está analizando datos en tiempo real. Selecciona un módulo en el menú lateral para comenzar tu sesión de trabajo.</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    if st.session_state['datasets'] is not None:
        st.info("✅ **Conexión con el Modelo:** RF-Optimizado v2.4")
        st.info("✅ **Estado de Datos:** Dataset Cargado Exitosamente")
    else:
        st.error("⚠️ Error: No se encontró el dataset en la carpeta /datasets/")

# 5. Acceso Rápido
st.markdown("---")
st.write("### 🚀 Acceso Rápido")
quick_links = st.columns(4)

# Nota: Los botones en Streamlit de multipágina no redirigen automáticamente sin lógica extra
# Se recomienda usar la barra lateral oficial para la navegación principal.
quick_links[0].button("📊 Dashboard")
quick_links[1].button("🧠 Detector")
quick_links[2].button("🔄 Simulador")
quick_links[3].button("📄 Reportes")
