import streamlit as st
import joblib
import numpy as np
import os

# Configuración de página centrada
st.set_page_config(page_title="Detector Integral", layout="centered")

# Estilos CSS estrictos para evitar el estiramiento
st.markdown("""
    <style>
    /* Centrar todo el contenido principal */
    .block-container { max-width: 600px !important; padding-top: 2rem; }
    
    /* Diseño de la tarjeta central */
    .card { 
        background-color: #1e1e26; 
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid #333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Botones profesionales */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.2em; 
        background-color: #4f46e5; 
        color: white; 
        border: none; 
        font-weight: bold; 
        margin-top: 10px;
    }
    .stButton>button:hover { background-color: #4338ca; }
    </style>
""", unsafe_allow_html=True)

# Contenedor con la clase CSS 'card'
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.title("🧠 Detector Integral")

    # 1. Estado de sesión
    if 'paso' not in st.session_state:
        st.session_state.update({'paso': -1, 'respuestas': []})

    # 2. Pantalla de Bienvenida
    if st.session_state.paso == -1:
        st.write("Bienvenido. Este sistema analiza tus hábitos académicos mediante IA para estimar tus niveles de estrés.")
        if st.button("🚀 Iniciar Evaluación"):
            st.session_state.paso = 0
            st.rerun()

    # 3. Flujo del Test
    elif st.session_state.paso < 8:
        preguntas = [
            "¿Cuál es tu nivel de ansiedad actual?",
            "¿Qué nivel de confianza tienes en ti mismo/a?",
            "¿Cómo calificarías tu estado de ánimo general?",
            "¿Cómo es la calidad de tu sueño?",
            "¿Qué capacidad tienes para manejar tu carga de estudio?",
            "¿Qué tanto tiempo dedicas a actividades recreativas?",
            "¿Cuánto apoyo social sientes que recibes?",
            "¿Cómo es tu interés académico?"
        ]
        
        st.caption(f"Pregunta {st.session_state.paso + 1} de 8")
        st.progress((st.session_state.paso) / 8)
        
        val = st.slider(preguntas[st.session_state.paso], 1, 10, 5, label_visibility="visible")
        
        if st.button("Siguiente →"):
            st.session_state.respuestas.append(val)
            st.session_state.paso += 1
            st.rerun()

    # 4. Pantalla de Resultados
    else:
        modelo = joblib.load("modelos/modelo_stress_rf.pkl")
        estres = modelo.predict(np.array([st.session_state.respuestas]))[0]
        rend = 2 - estres
        
        st.subheader("📋 Resultados Finales")
        st.write(f"**Nivel de Estrés:** {['BAJO', 'MODERADO', 'ALTO'][estres]}")
        st.write(f"**Rendimiento Proyectado:** {['MALO', 'IRREGULAR', 'ALTO'][rend]}")
        
        st.markdown("---")
        st.write("💡 **Sugerencia:** " + ["Mantén hábitos saludables.", "Prioriza el descanso.", "Busca apoyo profesional."][estres])
        
        if st.button("🔄 Reiniciar"):
            st.session_state.update({'paso': -1, 'respuestas': []})
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
