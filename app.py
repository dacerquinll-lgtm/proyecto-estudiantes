import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="Plataforma de Bienestar Estudiantil",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Sistema de Análisis de Bienestar Estudiantil")
st.markdown("---")

if 'datasets' not in st.session_state:
    try:
        # Encontrar la ruta absoluta del proyecto de forma dinámica
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construcción de rutas compatibles tanto para Windows local como para Linux Cloud
        ruta_estres = os.path.join(base_dir, "datasets", "Estudiantes_Estres.csv")
        ruta_burnout = os.path.join(base_dir, "datasets", "Estudiantes_Burnout.csv")
        
        # Si no los encuentra ahí, busca archivos alternativos en la raíz por si se subieron plano
        if not os.path.exists(ruta_estres):
            ruta_estres = os.path.join(base_dir, "Estudiantes_Estres.csv")
        if not os.path.exists(ruta_burnout):
            ruta_burnout = os.path.join(base_dir, "Estudiantes_Burnout.csv")

        df_estres = pd.read_csv(ruta_estres)
        df_burnout = pd.read_csv(ruta_burnout)
        
        # Limpieza de nombres de columnas
        df_estres.columns = df_estres.columns.str.strip().str.lower()
        df_burnout.columns = df_burnout.columns.str.strip().str.lower()
        
        st.session_state.datasets = {
            'estres': df_estres,
            'burnout': df_burnout
        }
        st.success("¡Datos cargados exitosamente de forma dinámica!")
    except Exception as e:
        st.error(f"Error al cargar los archivos CSV: {e}")

if 'modelos' not in st.session_state:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_modelo = os.path.join(base_dir, "modelos", "modelo_estres.pkl")
        
        if not os.path.exists(ruta_modelo):
            ruta_modelo = os.path.join(base_dir, "modelo_estres.pkl")
            
        st.session_state.modelos = {
            'estres': joblib.load(ruta_modelo)
        }
    except Exception as e:
        st.warning(f"Nota: Modelo predictivo no detectado o en mantenimiento. ({e})")

st.markdown("""
### ¡Bienvenido a la Plataforma Analítica!
Use el menú lateral de la izquierda para explorar los diferentes módulos interactivos del sistema.
""")
