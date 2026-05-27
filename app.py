import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Plataforma de Bienestar Estudiantil",
    page_icon="🎓",
    layout="wide"
)

if 'datasets' not in st.session_state:
    st.session_state.datasets = {}

def cargar_datos_extendido(nombre_clave, ruta_relativa):
    if nombre_clave not in st.session_state.datasets:
        if os.path.exists(ruta_relativa):
            df = pd.read_csv(ruta_relativa)
            st.session_state.datasets[nombre_clave] = df
        else:
            st.session_state.datasets[nombre_clave] = None
    return st.session_state.datasets[nombre_clave]

df1 = cargar_datos_extendido('estres', 'datasets/StressLevelDataset_limpio.csv')
df2 = cargar_datos_extendido('burnout', 'datasets/student_mental_health_burnout_10k.csv')

st.title("🎓 Sistema Inteligente de Monitoreo y Bienestar Estudiantil")
st.markdown("---")

st.markdown("""
### ¡Bienvenido a la Plataforma Avanzada de Analítica de Datos!
Esta herramienta utiliza Inteligencia Artificial para evaluar, predecir y mejorar la calidad de vida académica de los estudiantes mediante dos motores algorítmicos integrados.

#### Estructura del Sistema (Vistas Disponibles):
1. **🏠 Inicio (Esta vista):** Introducción general e indicadores globales del estado de carga del sistema.
2. **Dashboard General:** Exploración visual y descriptiva de las variables de Kaggle.
3. **Detector de Estrés:** Clasificador analítico basado en métricas psicológicas individuales.
4. **Motor de Recomendaciones:** Evaluador predictivo del nivel de Burnout estudiantil.
5. **Simulador de Estilo de Vida:** Herramienta interactiva para proyectar cambios de hábitos en tiempo real.
6. **Análisis Comparativo:** Módulo de correlación estadística.
7. **Reportes y Exportación:** Generador de resúmenes de datos personalizados.
""")

if df1 is not None and df2 is not None:
    st.success("Sistemas listos. Datos cargados y persistidos correctamente en la sesión global.")
else:
    st.warning("Archivos de datos locales no detectados en la carpeta /datasets. Por favor, verifica los nombres de los archivos.")