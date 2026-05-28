import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Detector de Niveles de Estrés")
st.markdown("---")

ruta_modelo = "modelos/modelo_stress_rf.pkl"

if os.path.exists(ruta_modelo):
    modelo = joblib.load(ruta_modelo)

    st.markdown("### Ingrese sus métricas actuales:")
    col1, col2 = st.columns(2)
    with col1:
        anx = st.slider("Ansiedad (1-10)", 1, 10, 5)
        self_e = st.slider("Autoestima (1-10)", 1, 10, 5)
        dep = st.slider("Depresión (1-10)", 1, 10, 5)
        sleep = st.slider("Calidad de Sueño (1-10)", 1, 10, 5)
        acad = st.slider("Rendimiento Académico (1-10)", 1, 10, 5)
    with col2:
        load = st.slider("Carga de Estudio (1-10)", 1, 10, 5)
        soc = st.slider("Apoyo Social (1-10)", 1, 10, 5)
        peer = st.slider("Presión de Pares (1-10)", 1, 10, 5)
        extra = st.slider("Actividades Extras (1-10)", 1, 10, 5)
        bull = st.slider("Experiencia de Bullying (1-10)", 1, 10, 5)

    if st.button("Obtener Diagnóstico y Recomendaciones"):
        datos_usuario = [anx, self_e, dep, sleep, acad, load, soc, peer, extra, bull]
        prediccion = modelo.predict(np.array([datos_usuario]))[0]
        
        # Guardamos en session_state para el reporte
        st.session_state['ultimo_diagnostico'] = {
            'datos': datos_usuario,
            'resultado': prediccion
        }
        
        st.subheader("📋 Resultados del Análisis")
        if prediccion == 0:
            st.success("Nivel de Estrés: BAJO")
            rec = "Mantén tus hábitos actuales. Tu equilibrio es positivo."
            esc = "Si reduces tus horas de sueño, tu estrés podría subir a Moderado."
        elif prediccion == 1:
            st.warning("Nivel de Estrés: MODERADO")
            rec = "Prioriza tus tiempos de descanso y organiza mejor tu carga académica."
            esc = "Si aumentas tu apoyo social, podrías estabilizar tu estrés a un nivel Bajo."
        else:
            st.error("Nivel de Estrés: ALTO")
            rec = "Es crucial buscar apoyo profesional y reducir tareas no esenciales inmediatamente."
            esc = "Si mantienes este ritmo sin descanso, el riesgo de agotamiento académico es crítico."
        
        st.markdown("---")
        st.info(f"💡 **Recomendación:** {rec}")
        st.warning(f"🔮 **Escenario futuro:** {esc}")
        st.success("✅ Diagnóstico guardado. Ya puedes generar tu reporte en la página de Reportes.")
else:
    st.error("El modelo de estrés no está disponible. Verifica la carpeta /modelos.")
