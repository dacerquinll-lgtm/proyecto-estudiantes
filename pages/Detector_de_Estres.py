import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Detector Integral Académico")

# Inicializar sesión
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': []})

preguntas = [
    ("¿Cuál es tu nivel de ansiedad? (1-10)", 5),
    ("¿Cómo calificarías tu autoestima? (1-10)", 5),
    ("¿Qué nivel de depresión sientes? (1-10)", 5),
    ("¿Cómo es tu calidad de sueño? (1-10)", 5),
    ("¿Qué carga de estudio tienes? (1-10)", 5),
    ("¿Nivel de actividades extras? (1-10)", 5),
    ("¿Cuánto apoyo social recibes? (1-10)", 5),
    ("¿Cuál es tu rendimiento académico previo? (1-10)", 5)
]

# Flujo de cuestionario
if st.session_state.paso < len(preguntas):
    st.subheader(f"Pregunta {st.session_state.paso + 1} de {len(preguntas)}")
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()
else:
    # 1. Predicción del modelo
    modelo = joblib.load("modelos/modelo_stress_rf.pkl")
    datos = np.array([st.session_state.respuestas])
    estres = modelo.predict(datos)[0] # 0, 1, o 2
    
    # 2. Lógica de rendimiento (Consecuencia del Estrés)
    # Estrés 0 (Bajo) -> Rendimiento 2 (Alto)
    # Estrés 1 (Mod) -> Rendimiento 1 (Irregular)
    # Estrés 2 (Alto) -> Rendimiento 0 (Malo)
    rendimiento = 2 - estres
    
    # 3. Mostrar resultados
    st.subheader("📋 Resultados Finales")
    st.write(f"**Nivel de Estrés Detectado:** {['BAJO', 'MODERADO', 'ALTO'][estres]}")
    st.write(f"**Proyección de Rendimiento:** {['MALO', 'IRREGULAR', 'ALTO'][rendimiento]}")
    
    st.markdown("---")
    st.info(f"💡 Recomendación: {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
    st.info(f"💡 Análisis Académico: {['Necesitas tutorías extra.', 'Organiza mejor tus tiempos.', '¡Excelente ritmo, continúa así!'][rendimiento]}")

    if st.button("Reiniciar"):
        st.session_state.update({'paso': 0, 'respuestas': []})
        st.rerun()
