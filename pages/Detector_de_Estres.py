import streamlit as st
import joblib
import numpy as np
import os

# Configuración: Layout 'centered' hace el trabajo duro de centrar todo
st.set_page_config(page_title="Detector Integral", layout="centered")

st.title("🧠 Detector Integral Académico")

# 1. Inicialización
if 'paso' not in st.session_state:
    st.session_state.update({'paso': -1, 'respuestas': []})

# 2. Pantalla de Bienvenida
if st.session_state.paso == -1:
    st.markdown("### Bienvenido al sistema de evaluación")
    st.write("Este sistema utiliza inteligencia artificial para analizar tus hábitos académicos. Responde con honestidad las 8 preguntas para obtener una proyección precisa.")
    
    if st.button("🚀 Comenzar Evaluación"):
        st.session_state.paso = 0
        st.rerun()

# 3. Flujo del Test
elif st.session_state.paso < 8:
    preguntas = [
        "¿Cuál es tu nivel de ansiedad actual? (1=Extrema, 10=Ninguna)",
        "¿Qué nivel de confianza tienes en ti mismo/a? (1=Muy baja, 10=Muy alta)",
        "¿Cómo calificarías tu estado de ánimo general? (1=Muy decaído, 10=Muy optimista)",
        "¿Cómo es la calidad de tu sueño? (1=Muy mala, 10=Excelente)",
        "¿Qué capacidad tienes para manejar tu carga de estudio? (1=Desbordado, 10=Control total)",
        "¿Qué tanto tiempo dedicas a actividades recreativas? (1=Nada, 10=Lo suficiente)",
        "¿Cuánto apoyo social sientes que recibes? (1=Nada, 10=Muchísimo)",
        "¿Cómo es tu interés académico? (1=Muy bajo, 10=Excelente)"
    ]
    
    st.subheader(f"Pregunta {st.session_state.paso + 1} de 8")
    st.progress((st.session_state.paso) / 8)
    
    val = st.slider(preguntas[st.session_state.paso], 1, 10, 5)
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

# 4. Pantalla de Resultados
else:
    # Cargar modelo (asegúrate que la ruta sea correcta)
    modelo = joblib.load("modelos/modelo_stress_rf.pkl")
    estres = modelo.predict(np.array([st.session_state.respuestas]))[0]
    rend = 2 - estres
    
    st.subheader("📋 Resultados de tu Evaluación")
    
    # KPIs visuales simples pero elegantes
    col1, col2 = st.columns(2)
    col1.metric("Estrés Detectado", ["BAJO", "MODERADO", "ALTO"][estres])
    col2.metric("Rendimiento Proyectado", ["MALO", "IRREGULAR", "ALTO"][rend])
    
    st.markdown("---")
    st.info("💡 **Recomendación:** " + ["Mantén hábitos saludables.", "Prioriza el descanso.", "Busca apoyo profesional."][estres])
    
    if st.button("🔄 Reiniciar Evaluación"):
        st.session_state.update({'paso': -1, 'respuestas': []})
        st.rerun()
