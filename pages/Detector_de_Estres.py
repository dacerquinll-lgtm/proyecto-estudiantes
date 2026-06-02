import streamlit as st
import joblib
import numpy as np
import os

# Configuración de página
st.set_page_config(page_title="Detector Integral", layout="centered")

# Estilos CSS mejorados
st.markdown("""
    <style>
    .main-container { padding: 2rem; border-radius: 15px; background-color: #1e1e26; border: 1px solid #333; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4f46e5; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #4338ca; }
    h1 { color: #ffffff !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Contenedor principal para evitar saltos visuales
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.title("🧠 Detector Integral Académico")

    # 1. Inicialización
    if 'paso' not in st.session_state:
        st.session_state.update({'paso': -1, 'respuestas': []})

    # 2. Pantalla de Bienvenida
    if st.session_state.paso == -1:
        st.info("Bienvenido. Este sistema analiza tus hábitos académicos mediante IA para estimar tus niveles de estrés.")
        if st.button("🚀 Iniciar Evaluación"):
            st.session_state.paso = 0
            st.rerun()

    # 3. Flujo del Test
    elif st.session_state.paso < 8:
        preguntas = [
            "¿Cuál es tu nivel de ansiedad actual? (1=Extrema, 10=Ninguna)",
            "¿Qué nivel de confianza tienes en ti mismo/a? (1=Muy baja, 10=Muy alta)",
            "¿Cómo calificarías tu estado de ánimo general? (1=Muy decaído, 10=Muy optimista)",
            "¿Cómo es la calidad de tu sueño? (1=Muy mala, 10=Excelente)",
            "¿Qué capacidad tienes para manejar tu carga de estudio? (1=Desbordado/a, 10=Control total)",
            "¿Qué tanto tiempo dedicas a actividades recreativas? (1=Nada, 10=Lo suficiente)",
            "¿Cuánto apoyo social sientes que recibes? (1=Nada, 10=Muchísimo)",
            "¿Cómo es tu interés académico? (1=Muy bajo, 10=Excelente)"
        ]
        
        st.write(f"Pregunta {st.session_state.paso + 1} de 8")
        st.progress((st.session_state.paso) / 8)
        
        val = st.slider(preguntas[st.session_state.paso], 1, 10, 5)
        
        if st.button("Siguiente →"):
            st.session_state.respuestas.append(val)
            st.session_state.paso += 1
            st.rerun()

    # 4. Pantalla de Resultados
    else:
        modelo = joblib.load("modelos/modelo_stress_rf.pkl")
        estres = modelo.predict(np.array([st.session_state.respuestas]))[0]
        rendimiento = 2 - estres
        
        colores = {0: "#00cc96", 1: "#ffa15a", 2: "#ef553b"}
        etiquetas_estres = ["BAJO", "MODERADO", "ALTO"]
        etiquetas_rend = ["MALO", "IRREGULAR", "ALTO"]

        st.subheader("📋 Resultados de tu Evaluación")
        st.metric("Nivel de Estrés Detectado", etiquetas_estres[estres])
        st.metric("Proyección de Rendimiento", etiquetas_rend[rendimiento])
        
        st.markdown("---")
        st.write(f"**Recomendación:** {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
        
        if st.button("🔄 Reiniciar Evaluación"):
            st.session_state.update({'paso': -1, 'respuestas': []})
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
