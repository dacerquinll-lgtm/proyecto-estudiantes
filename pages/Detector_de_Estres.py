import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Detector Integral Académico")

if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': []})

preguntas = [
    ("¿Cuál es tu nivel de ansiedad hoy? (1-10)", 5),
    ("¿Cómo calificarías tu autoestima? (1-10)", 5),
    ("¿Qué nivel de depresión sientes? (1-10)", 5),
    ("¿Cómo es tu calidad de sueño? (1-10)", 5),
    ("¿Qué carga de estudio tienes? (1-10)", 5),
    ("¿Nivel de actividades extras? (1-10)", 5),
    ("¿Cuánto apoyo social recibes? (1-10)", 5),
    ("¿Cuál es tu interés académico actual? (1-10)", 5)
]

if st.session_state.paso < len(preguntas):
    st.subheader(f"Pregunta {st.session_state.paso + 1} de {len(preguntas)}")
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()
else:
    modelo = joblib.load("modelos/modelo_stress_rf.pkl")
    datos = np.array([st.session_state.respuestas])
    
    # 1. Rendimiento (Modelo ML)
    pred_rend = modelo.predict(datos)[0]
    
    # 2. Estrés (Inferencia Lógica)
    suma = st.session_state.respuestas[0] + st.session_state.respuestas[2]
    estres = 2 if suma >= 15 else (1 if suma >= 8 else 0)

    st.subheader("📋 Resultados Finales")
    st.write(f"**Nivel de Estrés:** {['BAJO', 'MODERADO', 'ALTO'][estres]}")
    st.write(f"**Proyección de Rendimiento:** {['MALO', 'IRREGULAR', 'ALTO'][pred_rend]}")
    
    st.info(f"💡 Sugerencia Estrés: {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
    st.info(f"💡 Sugerencia Académica: {['Necesitas tutorías.', 'Organiza mejor tus tiempos.', '¡Excelente ritmo!'][pred_rend]}")

    if st.button("Reiniciar"):
        st.session_state.update({'paso': 0, 'respuestas': []})
        st.rerun()
