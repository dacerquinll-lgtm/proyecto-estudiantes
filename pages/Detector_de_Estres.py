import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Detector Integral", layout="centered")

# CSS para limpiar cualquier residuo visual
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] { border: none !important; }
    hr { display: none !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Detector Integral Académico")

if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})

if not st.session_state.iniciado:
    st.write("Bienvenido al sistema de evaluación.")
    st.write("Este sistema implementa modelos de **Aprendizaje Automático** para analizar tus hábitos académicos.")
    if st.button("🚀 Comenzar Test"):
        st.session_state.iniciado = True
        st.rerun()

elif st.session_state.paso < 8:
    # Usamos esto en lugar de subheader/markdown para que no aparezca ninguna línea
    st.write(f"**Pregunta {st.session_state.paso + 1} de 8**")
    st.progress((st.session_state.paso) / 8)
    
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
    
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

else:
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    if os.path.exists(ruta_modelo):
        modelo = joblib.load(ruta_modelo)
        estres = modelo.predict(np.array([st.session_state.respuestas]))[0]
        rendimiento = 2 - estres
        
        st.write("**Resultados Finales**")
        col1, col2 = st.columns(2)
        col1.metric("Estrés", ["BAJO", "MODERADO", "ALTO"][estres])
        col2.metric("Rendimiento", ["MALO", "IRREGULAR", "ALTO"][rendimiento])
        
        st.info(f"💡 **Recomendación:** {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
        if estres == 2:
            st.warning("⚠️ **Atención:** Se recomienda contactar con Bienestar Universitario.")
            
    if st.button("🔄 Reiniciar"):
        st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})
        st.rerun()
