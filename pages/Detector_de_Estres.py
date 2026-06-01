import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Diagnóstico de Interés Académico")

# Inicializar estado para guardar respuestas
if 'paso' not in st.session_state:
    st.session_state.paso = 0
    st.session_state.respuestas = []

# Definir las preguntas
preguntas = [
    ("¿Cuál es tu nivel de ansiedad hoy? (1-10)", 5),
    ("¿Cómo calificarías tu autoestima? (1-10)", 5),
    ("¿Sientes niveles de depresión? (1-10)", 5),
    ("¿Cómo calificarías tu calidad de sueño? (1-10)", 5),
    ("¿Qué carga de estudio tienes actualmente? (1-10)", 5),
    ("¿Participas en actividades extracurriculares? (1-10)", 5),
    ("¿Cómo calificarías tu interés académico? (1-10)", 5),
    ("¿Qué tanto apoyo social recibes? (1-10)", 5)
]

# Lógica del cuestionario paso a paso
if st.session_state.paso < len(preguntas):
    pregunta_texto, valor_default = preguntas[st.session_state.paso]
    st.subheader(f"Pregunta {st.session_state.paso + 1} de {len(preguntas)}")
    
    # Capturar respuesta
    respuesta = st.slider(pregunta_texto, 1, 10, valor_default)
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(respuesta)
        st.session_state.paso += 1
        st.rerun()
else:
    # Procesar resultados al terminar
    modelo = joblib.load("modelos/modelo_stress_rf.pkl")
    datos_usuario = np.array([st.session_state.respuestas])
    
    prediccion_bruta = modelo.predict(datos_usuario)[0]
    
    # Capa de lógica de seguridad
    if st.session_state.respuestas[0] >= 9 and st.session_state.respuestas[1] <= 2:
        prediccion_final = 0
    else:
        prediccion_final = prediccion_bruta

    st.subheader("📋 Resultados del Análisis")
    resultados = {0: "BAJO", 1: "MEDIO", 2: "ALTO"}
    st.success(f"Nivel de Interés Académico Proyectado: **{resultados[prediccion_final]}**")
    
    if st.button("Reiniciar Cuestionario"):
        st.session_state.paso = 0
        st.session_state.respuestas = []
        st.rerun()
