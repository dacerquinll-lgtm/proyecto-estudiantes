import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Detector Integral", layout="centered")

# CSS para darle el estilo de "tarjeta" profesional
st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .card { background-color: #262730; padding: 20px; border-radius: 15px; border: 1px solid #4f46e5; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Detector Integral Académico")

if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})

# --- PANTALLA DE BIENVENIDA ---
if not st.session_state.iniciado:
    st.markdown("---")
    st.markdown("### 🎯 Sistema de Evaluación Inteligente")
    st.write("Este sistema utiliza **Aprendizaje Automático (Machine Learning)** para analizar tus patrones de comportamiento académico.")
    if st.button("🚀 Comenzar Evaluación"):
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
    
    st.progress((st.session_state.paso) / 8)
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    
    if st.button("Siguiente ➡️"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

# --- RESULTADOS PROFESIONALES ---
else:
    modelo = joblib.load("modelos/modelo_stress_rf.pkl")
    estres = modelo.predict(np.array([st.session_state.respuestas]))[0]
    rend = 2 - estres
    
    # Colores según el nivel
    colores = ["#00cc96", "#ffa15a", "#ef553b"] # Verde, Naranja, Rojo
    etiquetas = ["BAJO", "MODERADO", "ALTO"]
    
    st.subheader("📋 Informe de Resultados")
    
    # Tarjeta de resultado principal
    st.markdown(f"""
    <div class="card">
        <p>Nivel de Estrés Detectado:</p>
        <h1 style="color: {colores[estres]};">{etiquetas[estres]}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.metric("Proyección de Rendimiento", ["MALO", "IRREGULAR", "ALTO"][rend])
    
    st.markdown("---")
    st.success(f"💡 **Recomendación:** {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
    
    if st.button("🔄 Reiniciar Evaluación"):
        st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})
        st.rerun()
