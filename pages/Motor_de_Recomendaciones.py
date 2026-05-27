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
        
        st.markdown("### Ingrese los 10 parámetros de evaluación:")
        
        col1, col2 = st.columns(2)
        with col1:
            anxiety = st.slider("1. Nivel de Ansiedad (1-10):", 1, 10, 5)
            self_esteem = st.slider("2. Autoestima (1-10):", 1, 10, 5)
            depression = st.slider("3. Nivel de Depresión (1-10):", 1, 10, 5)
            sleep_q = st.slider("4. Calidad de Sueño (1-10):", 1, 10, 5)
            academic = st.slider("5. Rendimiento Académico (1-10):", 1, 10, 5)
        with col2:
            study_load = st.slider("6. Carga de Estudio (1-10):", 1, 10, 5)
            social = st.slider("7. Apoyo Social (1-10):", 1, 10, 5)
            peer = st.slider("8. Presión de Pares (1-10):", 1, 10, 5)
            extra = st.slider("9. Actividades Extras (1-10):", 1, 10, 5)
            bullying = st.slider("10. Experiencia de Bullying (1-10):", 1, 10, 5)
        
        if st.button("Calcular Diagnóstico"):
            # Array de 10 elementos exactos
            data = np.array([[anxiety, self_esteem, depression, sleep_q, academic, 
                             study_load, social, peer, extra, bullying]])
            
            prediccion = modelo.predict(data)
            st.metric(label="Nivel de Estrés Predicho", value=f"Nivel {prediccion[0]}")
            
    except Exception as e:
        st.error(f"Error al ejecutar el modelo: {e}")
else:
    st.error("No se encuentra 'modelo_stress_rf.pkl'. Asegúrate de que esté en la carpeta /modelos.")
