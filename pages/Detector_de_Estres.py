import streamlit as st
import joblib
import os
import numpy as np

st.title("🧠 Detector de Niveles de Estrés Analítico")
st.markdown("---")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_modelo = os.path.join(base_dir, "modelos", "modelo_stress_rf.pkl")

if os.path.exists(ruta_modelo):
    try:
        modelo = joblib.load(ruta_modelo)
        st.success("Modelo Predictivo Random Forest acoplado correctamente.")
        
        st.markdown("### Ingrese los 10 parámetros de evaluación:")
        
        # Creamos columnas para organizar mejor la entrada
        c1, c2 = st.columns(2)
        with c1:
            anxiety = st.slider("Nivel de Ansiedad (1-10):", 1, 10, 5)
            self_esteem = st.slider("Autoestima (1-10):", 1, 10, 5)
            depression = st.slider("Nivel de Depresión (1-10):", 1, 10, 5)
            sleep_quality = st.slider("Calidad de Sueño (1-10):", 1, 10, 5)
            academic_perf = st.slider("Rendimiento Académico (1-10):", 1, 10, 5)
        with c2:
            study_load = st.slider("Carga de Estudio (1-10):", 1, 10, 5)
            social_supp = st.slider("Apoyo Social (1-10):", 1, 10, 5)
            peer_pressure = st.slider("Presión de Pares (1-10):", 1, 10, 5)
            extra_act = st.slider("Actividades Extracurriculares (1-10):", 1, 10, 5)
            bullying = st.slider("Experiencia de Bullying (1-10):", 1, 10, 5)
        
        if st.button("Calcular Diagnóstico"):
            # Creamos el array con los 10 valores en el orden exacto del entrenamiento
            features = np.array([[
                anxiety, self_esteem, depression, sleep_quality, 
                academic_perf, study_load, social_supp, 
                peer_pressure, extra_act, bullying
            ]])
            
            prediccion = modelo.predict(features)
            st.metric(label="Nivel de Estrés Predicho", value=f"Nivel {prediccion[0]}")
            
    except Exception as e:
        st.error(f"Error al ejecutar el modelo: {e}")
else:
    st.warning(f"Archivo de modelo no detectado en: {ruta_modelo}")
