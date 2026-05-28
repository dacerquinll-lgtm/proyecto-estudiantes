import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Detector de Niveles de Estrés")
st.markdown("---")

ruta_modelo = "modelos/modelo_stress_rf.pkl"
modelo = joblib.load(ruta_modelo)

st.markdown("### Ingrese sus métricas actuales:")
col1, col2 = st.columns(2)
with col1:
    anxiety = st.slider("Ansiedad (1-10)", 1, 10, 5)
    self_esteem = st.slider("Autoestima (1-10)", 1, 10, 5)
    depression = st.slider("Depresión (1-10)", 1, 10, 5)
    sleep_q = st.slider("Calidad de Sueño (1-10)", 1, 10, 5)
    academic = st.slider("Rendimiento Académico (1-10)", 1, 10, 5)
with col2:
    study_load = st.slider("Carga de Estudio (1-10)", 1, 10, 5)
    social = st.slider("Apoyo Social (1-10)", 1, 10, 5)
    peer = st.slider("Presión de Pares (1-10)", 1, 10, 5)
    extra = st.slider("Actividades Extras (1-10)", 1, 10, 5)
    bullying = st.slider("Experiencia de Bullying (1-10)", 1, 10, 5)

if st.button("Obtener Diagnóstico y Recomendaciones"):
    data = np.array([[anxiety, self_esteem, depression, sleep_q, academic, 
                     study_load, social, peer, extra, bullying]])
    
    prediccion = modelo.predict(data)[0]
    
    # 1. RESULTADOS
    st.subheader("📋 Resultados del Análisis")
    if prediccion == 0:
        st.success("Nivel de Estrés: BAJO")
        recomendacion = "Mantén tus hábitos actuales. Tu equilibrio es positivo."
        escenario = "Si reduces tus horas de sueño, tu estrés podría subir a Moderado."
    elif prediccion == 1:
        st.warning("Nivel de Estrés: MODERADO")
        recomendacion = "Prioriza tus tiempos de descanso y organiza mejor tu carga académica."
        escenario = "Si aumentas tu apoyo social, podrías estabilizar tu estrés a un nivel Bajo."
    else:
        st.error("Nivel de Estrés: ALTO")
        recomendacion = "Es crucial buscar apoyo profesional y reducir tareas no esenciales inmediatamente."
        escenario = "Si mantienes este ritmo sin descanso, el riesgo de agotamiento académico es crítico."
    
    # 2. RECOMENDACIONES Y ESCENARIOS
    st.markdown("---")
    st.info(f"💡 **Recomendación:** {recomendacion}")
    st.warning(f"🔮 **Escenario futuro:** {escenario}")
