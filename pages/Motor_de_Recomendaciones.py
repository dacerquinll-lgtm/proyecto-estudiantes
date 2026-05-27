import streamlit as st
import joblib
import numpy as np
import os

st.title("🌱 Motor de Recomendaciones y Evaluación de Burnout")
st.markdown("---")

ruta_modelo = "modelos/modelo_burnout_rf.pkl"

if os.path.exists(ruta_modelo):
    model = joblib.load(ruta_modelo)
    
    st.markdown("### Responda a las siguientes preguntas sobre su rutina diaria:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cgpa = st.slider("Promedio Académico Actual (CGPA de 0.0 a 10.0)", 0.0, 10.0, 7.5, step=0.1)
        stress_level = st.slider("Nivel de Estrés Percibido (1 a 10)", 1, 10, 5)
        sleep_hours = st.slider("Horas de Sueño Promedio por Noche", 4, 10, 7)
        workload = st.slider("Carga de Trabajo/Estudio Semanal (Horas)", 10, 60, 30)
        
    with col2:
        financial_stress = st.slider("Nivel de Estrés Financiero (1 a 5)", 1, 5, 3)
        extracurricular = st.slider("Horas Semanales en Actividades Extracurriculares", 0, 20, 5)
        history_mental = st.selectbox("¿Tiene antecedentes personales de problemas de salud mental?", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
        history_family = st.selectbox("¿Tiene antecedentes familiares de problemas de salud mental?", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
    
    st.markdown("---")
    
    if st.button("Generar Evaluación y Recomendaciones"):
        caracteristicas = np.array([[
            cgpa, stress_level, sleep_hours, workload,
            financial_stress, extracurricular, history_mental, history_family
        ]])
        
        prediccion_burnout = model.predict(caracteristicas)[0]
        
        st.subheader("📋 Diagnóstico y Plan de Acción Personalizado")
        
        if prediccion_burnout < 3.5:
            st.success(f"Índice de Burnout Calculado: {prediccion_burnout:.2f} (Bajo)")
            st.markdown("""
            **Recomendaciones para mantener tu buen ritmo:**
            * **Mantén tu rutina:** Tus hábitos actuales de sueño y organización te están dando excelentes resultados.
            * **Fija límites saludables:** Sigue respetando tus espacios de descanso aunque aumente la carga del ciclo académico.
            * **Planificación anticipada:** Continúa distribuyendo tus tareas con tiempo para evitar picos de presión imprevistos.
            """)
            
        elif 3.5 <= prediccion_burnout <= 7.0:
            st.warning(f"Índice de Burnout Calculado: {prediccion_burnout:.2f} (Moderado)")
            st.markdown("""
            **Plan de acción preventivo:**
            * **Optimiza tu higiene del sueño:** Intenta regularizar tu hora de acostarte y asegurar un mínimo de 7 horas diarias.
            * **Técnicas de gestión del tiempo:** Aplica métodos como la técnica Pomodoro para estudiar en bloques enfocados y evitar la fatiga mental.
            * **Priorización de tareas:** Clasifica tus pendientes usando la matriz de Eisenhower (Urgente vs. Importante) para reducir la sobrecarga semanal.
            """)
            
        else:
            st.error(f"Índice de Burnout Calculado: {prediccion_burnout:.2f} (Alto)")
            st.markdown("""
            **Alerta de Bienestar - Medidas prioritarias:**
            * **Pausa estratégica inmediata:** Reduce en la medida de lo posible las actividades extracurriculares no esenciales durante esta semana.
            * **Establece redes de apoyo:** Conversa sobre tu estado actual con tus familiares, amigos cercanos o docentes de confianza.
            * **Orientación institucional:** Te sugerimos agendar una cita con el área de tutoría o apoyo psicológico de la universidad para recibir herramientas profesionales de contención.
            """)
else:
    st.error("El archivo binario del modelo ('modelo_burnout_rf.pkl') no se encuentra en la carpeta /modelos.")