import streamlit as st
import joblib
import numpy as np
import os

st.title("🌱 Motor de Recomendaciones y Evaluación de Burnout")
st.markdown("---")

# Ajuste: Asegurar que la ruta sea relativa al archivo actual
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_modelo = os.path.join(base_dir, "modelos", "modelo_burnout_rf.pkl")

if os.path.exists(ruta_modelo):
    model = joblib.load(ruta_modelo)
    
    st.markdown("### Responda a las siguientes preguntas sobre su rutina diaria:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Correspondencia con tus 7 variables de entrenamiento:
        sleep = st.slider("Horas de Sueño:", 4, 10, 7) # 'sleep'
        physical = st.slider("Nivel de Actividad Física (1-10):", 1, 10, 5) # 'physical'
        social = st.slider("Interacción Social (1-10):", 1, 10, 5) # 'social'
        academic = st.slider("Desempeño Académico (1-10):", 1, 10, 5) # 'academic'
        
    with col2:
        anxiety = st.slider("Nivel de Ansiedad (1-10):", 1, 10, 5) # 'anxiety'
        depres = st.slider("Nivel de Depresión (1-10):", 1, 10, 5) # 'depres'
        lifestyle = st.slider("Calidad de Estilo de Vida (1-10):", 1, 10, 5) # 'lifestyle'
    
    st.markdown("---")
    
    if st.button("Generar Evaluación y Recomendaciones"):
        # Enviamos las 7 variables en el orden exacto de tu script de entrenamiento
        caracteristicas = np.array([[
            sleep, physical, social, academic, 
            anxiety, depres, lifestyle
        ]])
        
        prediccion_burnout = model.predict(caracteristicas)[0]
        
        st.subheader("📋 Diagnóstico y Plan de Acción")
        
        if prediccion_burnout < 3.5:
            st.success(f"Índice: {prediccion_burnout:.2f} (Bajo)")
            st.markdown("*Mantén tu rutina, tus hábitos actuales son excelentes.*")
        elif 3.5 <= prediccion_burnout <= 7.0:
            st.warning(f"Índice: {prediccion_burnout:.2f} (Moderado)")
            st.markdown("*Intenta optimizar tu gestión del tiempo y descanso.*")
        else:
            st.error(f"Índice: {prediccion_burnout:.2f} (Alto)")
            st.markdown("*Prioriza tu bienestar; te sugerimos una pausa estratégica.*")

else:
    st.error(f"El modelo no se encuentra en: {ruta_modelo}")
