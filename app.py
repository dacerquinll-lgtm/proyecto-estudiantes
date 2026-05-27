import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Plataforma de Bienestar Estudiantil",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Sistema de Análisis de Bienestar Estudiantil")
st.markdown("---")

if 'datasets' not in st.session_state:
    try:
        df_estres = pd.read_csv("datasets/Estudiantes_Estres.csv")
        df_burnout = pd.read_csv("datasets/Estudiantes_Burnout.csv")
        
        # Forzar minúsculas y quitar espacios en blanco en los nombres de columnas
        df_estres.columns = df_estres.columns.str.strip().str.lower()
        df_burnout.columns = df_burnout.columns.str.strip().str.lower()
        
        st.session_state.datasets = {
            'estres': df_estres,
            'burnout': df_burnout
        }
    except Exception as e:
        st.error(f"Error al cargar los archivos CSV: {e}")

if 'modelos' not in st.session_state:
    try:
        st.session_state.modelos = {
            'estres': joblib.load("modelos/modelo_estres.pkl")
        }
    except Exception as e:
        st.warning(f"Nota: Modelo predictivo no detectado o en mantenimiento. ({e})")

st.markdown("""
### ¡Bienvenido a la Plataforma Analítica!
Use el menú lateral de la izquierda para explorar los diferentes módulos interactivos del sistema.
""")
