import streamlit as st
import joblib
import numpy as np
import os

# Configuración de página centrada
st.set_page_config(page_title="Detector Integral", layout="centered")

st.title("🧠 Detector Integral Académico")

# --- INICIALIZACIÓN ROBUSTA ---
if 'paso' not in st.session_state:
    st.session_state.paso = 0
    st.session_state.respuestas = []
    st.session_state.iniciado = False

# --- PANTALLA DE BIENVENIDA ---
if not st.session_state.iniciado:
    st.markdown("""
    ### Bienvenido al sistema de evaluación
    Este sistema implementa modelos de **Aprendizaje Automático (Machine Learning)** para analizar tus hábitos académicos y niveles de estrés. 
    Al completar este cuestionario, el algoritmo procesará tus variables para brindarte un diagnóstico proyectado y recomendaciones personalizadas.
    """)
    
    if st.button("🚀 Comenzar Test"):
        st.session_state.iniciado = True
        st.rerun()

# --- FLUJO DE CUESTIONARIO ---
elif st.session_state.paso < 8:
    preguntas = [
        ("¿Cuál es tu nivel de ansiedad actual? (1=Extrema, 10=Ninguna)", 5),
        ("¿Qué nivel de confianza tienes en ti mismo/a? (1=Muy baja, 10=Muy alta)", 5),
        ("¿Cómo calificarías tu estado de ánimo general? (1=Muy decaído, 10=Muy optimista)", 5),
        ("¿Cómo es la calidad de tu sueño? (1=Muy mala, 10=Excelente)", 5),
        ("¿Qué capacidad tienes para manejar tu carga de estudio? (1=Desbordado/a, 10=Control total)", 5),
        ("¿Qué tanto tiempo dedicas a actividades recreativas? (1=Nada, 10=Lo suficiente)", 5),
        ("¿Cuánto apoyo social sientes que recibes? (1=Nada, 10=Muchísimo)", 5),
        ("¿Cómo es tu interés académico? (1=Muy bajo, 10=Excelente)", 5)
    ]
    
    st.subheader(f"Pregunta {st.session_state.paso + 1} de 8")
    st.progress((st.session_state.paso) / 8)
    
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

# --- PANTALLA DE RESULTADOS PROFESIONAL ---
else:
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    if not os.path.exists(ruta_modelo):
        st.error(f"Error: No se encuentra el archivo en {ruta_modelo}")
        st.stop()
        
    modelo = joblib.load(ruta_modelo)
    estres = modelo.predict(np.array([st.session_state.respuestas]))[0] # 0: BAJO, 1: MODERADO, 2: ALTO
    rendimiento = 2 - estres 
    
    st.subheader("📋 Informe de Resultados")
    
    # Métricas visuales
    col1, col2 = st.columns(2)
    col1.metric("Nivel de Estrés", ["BAJO", "MODERADO", "ALTO"][estres])
    col2.metric("Proyección", ["MALO", "IRREGULAR", "ALTO"][rendimiento])
    
    st.markdown("---")
    
    # 1. Recomendación general según nivel
    recs = [
        "Mantén hábitos saludables y organiza tus tareas pendientes.",
        "Prioriza el descanso y aplica técnicas de gestión del tiempo.",
        "Es momento de tomar acción inmediata para proteger tu bienestar emocional."
    ]
    st.write(f"**Sugerencia Estratégica:** {recs[estres]}")
    
    # 2. Bloque EXTRA si el estrés es ALTO
    if estres == 2:
        st.warning("⚠️ **Nota de Atención Profesional:**")
        st.markdown("""
        Debido a que los indicadores sugieren un nivel de estrés elevado, te recomendamos:
        - **Buscar apoyo profesional:** Considera agendar una cita con el psicólogo del área de Bienestar Universitario.
        - **Desconexión:** Reduce actividades académicas no esenciales por 48 horas.
        - **Comunicación:** Habla con un tutor o docente de confianza sobre tu situación actual.
        *Tu salud es prioridad sobre cualquier calificación.*
        """)
    else:
        st.success("¡Excelente! Continúa monitoreando tu bienestar para mantener este equilibrio.")

    if st.button("🔄 Reiniciar Evaluación"):
        st.session_state.paso = 0
        st.session_state.respuestas = []
        st.session_state.iniciado = False
        st.rerun()
