import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Detector Integral", layout="centered")

# CSS para tarjetas y estilo moderno
st.markdown("""
    <style>
    .card { background-color: #262730; padding: 20px; border-radius: 15px; border-left: 5px solid #4f46e5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4f46e5; color: white; }
    </style>
""", unsafe_allow_html=True)

# Inicializar sesión
if 'paso' not in st.session_state:
    st.session_state.update({'paso': -1, 'respuestas': []})

# --- PANTALLA DE BIENVENIDA ---
if st.session_state.paso == -1:
    st.title("🧠 Detector Integral Académico")
    st.markdown("""
    <div class="card">
        <h3>Bienvenido al sistema de evaluación</h3>
        <p>Este sistema utiliza inteligencia artificial para analizar tu bienestar académico. 
        Por favor, responde con honestidad las 8 preguntas para obtener una proyección precisa.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Comenzar Test"):
        st.session_state.paso = 0
        st.rerun()

# --- FLUJO DE CUESTIONARIO ---
elif st.session_state.paso < 8:
    preguntas = [
        "Nivel de ansiedad actual (1=Extrema, 10=Ninguna)",
        "Nivel de confianza personal (1=Muy baja, 10=Muy alta)",
        "Estado de ánimo general (1=Muy decaído, 10=Muy optimista)",
        "Calidad de sueño (1=Muy mala, 10=Excelente)",
        "Capacidad de manejo de carga de estudio (1=Desbordado, 10=Control total)",
        "Tiempo dedicado a actividades recreativas (1=Nada, 10=Lo suficiente)",
        "Apoyo social percibido (1=Nada, 10=Muchísimo)",
        "Interés académico (1=Muy bajo, 10=Excelente)"
    ]
    
    st.progress((st.session_state.paso) / 8)
    val = st.slider(preguntas[st.session_state.paso], 1, 10, 5)
    
    if st.button("Siguiente →"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

# --- PANTALLA DE RESULTADOS PROFESIONAL ---
else:
    modelo = joblib.load("modelos/modelo_stress_rf.pkl")
    estres = modelo.predict(np.array([st.session_state.respuestas]))[0]
    
    # Mapeo de colores y etiquetas
    niveles = {0: ("BAJO", "#00cc96"), 1: ("MODERADO", "#ffa15a"), 2: ("ALTO", "#ef553b")}
    n_texto, n_color = niveles[estres]
    
    st.title("📊 Informe de Resultados")
    
    # Tarjeta de Diagnóstico
    st.markdown(f"""
        <div class="card">
            <h2 style="color: {n_color};">Nivel de Estrés: {n_texto}</h2>
            <p>El algoritmo ha procesado tus variables y determinado una alerta de nivel <b>{n_texto}</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### 📝 Análisis Detallado")
    with st.expander("Ver desglose técnico", expanded=True):
        st.write(f"- **Estado Académico:** El sistema identifica un patrón de rendimiento {'Alto' if estres == 0 else 'Irregular' if estres == 1 else 'Crítico'}.")
        st.write("- **Sugerencia estratégica:** " + ["Mantén tus hábitos de descanso.", "Considera reducir tu carga horaria.", "Es recomendable agendar una cita con bienestar universitario."][estres])

    if st.button("🔄 Reiniciar Evaluación"):
        st.session_state.update({'paso': -1, 'respuestas': []})
        st.rerun()
