import streamlit as st
import joblib
import numpy as np
import os

st.title("🌱 Motor de Recomendaciones y Evaluación de Burnout")
st.markdown("---")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_modelo = os.path.join(base_dir, "modelos", "modelo_burnout_rf.pkl")

if os.path.exists(ruta_modelo):
    model = joblib.load(ruta_modelo)
    
    st.markdown("### Responda las 6 preguntas para evaluar su estado:")
    
    col1, col2 = st.columns(2)
    with col1:
        val1 = st.slider("Sueño (sleep)", 1, 10, 7)
        val2 = st.slider("Físico (physical)", 1, 10, 5)
        val3 = st.slider("Social (social)", 1, 10, 5)
    with col2:
        val4 = st.slider("Académico (academic)", 1, 10, 5)
        val5 = st.slider("Ansiedad (anxiety)", 1, 10, 5)
        val6 = st.slider("Depresión (depres)", 1, 10, 5)
    
    if st.button("Generar Evaluación y Recomendaciones"):
        caracteristicas = np.array([[val1, val2, val3, val4, val5, val6]])
        
        try:
            pred = model.predict(caracteristicas)[0]
            st.subheader("📋 Diagnóstico y Plan de Acción")
            
            # Lógica de recomendaciones según el índice obtenido
            if pred < 3.5:
                st.success(f"Índice de Burnout: {pred:.2f} (Bajo)")
                st.write("**Recomendaciones:** Tu rutina es equilibrada. Mantén tus horarios de sueño y sigue priorizando actividades sociales que te generen bienestar.")
            elif 3.5 <= pred <= 6.5:
                st.warning(f"Índice de Burnout: {pred:.2f} (Moderado)")
                st.write("**Recomendaciones:** Estás empezando a acumular fatiga. Te sugerimos técnicas de gestión del tiempo (Pomodoro) y reducir ligeramente la carga de compromisos extracurriculares.")
            else:
                st.error(f"Índice de Burnout: {pred:.2f} (Alto)")
                st.write("**Recomendaciones:** Es vital priorizar tu salud mental. Reduce tareas no esenciales, busca apoyo con tutores académicos y considera hablar con un profesional de salud mental.")
                
        except Exception as e:
            st.error(f"Error al procesar: {e}")
else:
    st.error("No se encontró el modelo en la carpeta /modelos.")
