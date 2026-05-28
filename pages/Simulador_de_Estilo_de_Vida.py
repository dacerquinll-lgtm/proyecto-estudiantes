import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Detector de Niveles de Estrés")
st.markdown("---")

# Inicializamos la variable en el estado si no existe
if 'datos_usuario' not in st.session_state:
    st.session_state['datos_usuario'] = [5] * 10

ruta_modelo = "modelos/modelo_stress_rf.pkl"

if os.path.exists(ruta_modelo):
    modelo = joblib.load(ruta_modelo)
    
    # Usamos los datos guardados o valores por defecto
    d = st.session_state['datos_usuario']
    
    col1, col2 = st.columns(2)
    with col1:
        anx = st.slider("Ansiedad (1-10)", 1, 10, d[0])
        self_e = st.slider("Autoestima (1-10)", 1, 10, d[1])
        dep = st.slider("Depresión (1-10)", 1, 10, d[2])
        sleep = st.slider("Calidad de Sueño (1-10)", 1, 10, d[3])
        acad = st.slider("Rendimiento Académico (1-10)", 1, 10, d[4])
    with col2:
        load = st.slider("Carga de Estudio (1-10)", 1, 10, d[5])
        soc = st.slider("Apoyo Social (1-10)", 1, 10, d[6])
        peer = st.slider("Presión de Pares (1-10)", 1, 10, d[7])
        extra = st.slider("Actividades Extras (1-10)", 1, 10, d[8])
        bull = st.slider("Experiencia de Bullying (1-10)", 1, 10, d[9])

    if st.button("Obtener Diagnóstico y Recomendaciones"):
        datos_actuales = [anx, self_e, dep, sleep, acad, load, soc, peer, extra, bull]
        st.session_state['datos_usuario'] = datos_actuales # Guardamos para que el Simulador lo vea
        
        prediccion = modelo.predict(np.array([datos_actuales]))[0]
        st.session_state['ultimo_diagnostico'] = {'datos': datos_actuales, 'resultado': prediccion}
        
        st.success(f"Diagnóstico completado. Nivel detectado: {prediccion}")
else:
    st.error("Modelo no encontrado.")
