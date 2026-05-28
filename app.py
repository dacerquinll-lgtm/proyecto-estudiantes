
import streamlit as st
import pandas as pd
import os
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)





st.set_page_config(
    page_title="Plataforma de Bienestar Estudiantil",
    page_icon="🎓",
    layout="wide"
)

# Inicializar estado para datasets
if 'datasets' not in st.session_state:
    st.session_state.datasets = {}

def cargar_datos(nombre_clave, ruta_relativa):
    if nombre_clave not in st.session_state.datasets:
        if os.path.exists(ruta_relativa):
            df = pd.read_csv(ruta_relativa)
            st.session_state.datasets[nombre_clave] = df
        else:
            st.session_state.datasets[nombre_clave] = None
    return st.session_state.datasets[nombre_clave]

# Cargamos solo el dataset de estrés
df_estres = cargar_datos('estres', 'datasets/StressLevelDataset_limpio.csv')

st.title("🎓 Sistema Inteligente de Monitoreo de Bienestar Estudiantil")
st.markdown("---")

st.markdown("""
### ¡Bienvenido a la Plataforma de Analítica de Bienestar!
Esta herramienta utiliza Inteligencia Artificial para evaluar y proyectar el estado de salud mental de los estudiantes, enfocándose en la gestión del estrés académico.

#### Funcionalidades del Sistema:
* **Dashboard General:** Visualización del estado actual de los datos.
* **Detector de Estrés:** Diagnóstico preciso mediante modelos de aprendizaje automático.
* **Simulador de Escenarios:** Proyección interactiva de cambios en hábitos.
* **Análisis Comparativo:** Evaluación de correlaciones estadísticas.
* **Reportes y Exportación:** Gestión de resultados personalizados.
""")

if df_estres is not None:
    st.success("✅ Sistema listo. Dataset de bienestar cargado correctamente.")
else:
    st.warning("⚠️ El archivo 'StressLevelDataset_limpio.csv' no fue detectado en la carpeta /datasets. Verifica la ruta.")
