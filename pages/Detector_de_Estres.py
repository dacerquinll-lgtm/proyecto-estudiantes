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
            data = np.array([[anxiety, self_esteem, depression, sleep_q, academic, 
                             study_load, social, peer, extra, bullying]])
            
            prediccion = modelo.predict(data)[0]
            
            st.subheader("📋 Resultados del Análisis")
            
            if prediccion == 0:
                st.success("Nivel de Estrés: BAJO")
                st.write("**Descripción:** Tus indicadores muestran un estado de calma y equilibrio. Tu capacidad actual para gestionar las demandas académicas es óptima. ¡Continúa así!")
            elif prediccion == 1:
                st.warning("Nivel de Estrés: MODERADO")
                st.write("**Descripción:** Estás experimentando niveles de estrés que requieren atención. Es recomendable revisar tu organización y asegurar tiempos de descanso para evitar la fatiga acumulada.")
            else:
                st.error("Nivel de Estrés: ALTO")
                st.write("**Descripción (Advertencia):** Se han detectado indicadores significativos de estrés elevado. Es fundamental que reduzcas la carga de tareas no esenciales y busques apoyo institucional o profesional lo antes posible para proteger tu bienestar.")
            
    except Exception as e:
        st.error(f"Error al ejecutar el modelo: {e}")
else:
    st.error("No se encuentra el modelo de estrés. Asegúrate de que esté en la carpeta /modelos.")
