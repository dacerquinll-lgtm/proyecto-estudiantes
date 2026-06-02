import streamlit as st
import joblib
import numpy as np
import os

# Configuración de página centrada
st.set_page_config(page_title="Detector Integral", layout="centered")

# Estilo para asegurar que no haya líneas divisoras intrusivas
st.markdown("""
    <style>
    hr { display: none; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Detector Integral Académico")

# --- INICIALIZACIÓN ---
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})

# --- PANTALLA DE BIENVENIDA ---
if not st.session_state.iniciado:
    st.markdown("### Bienvenido al sistema de evaluación")
    st.write("Este sistema implementa modelos de **Aprendizaje Automático (Machine Learning)** para analizar tus hábitos académicos y niveles de estrés. Al completar este cuestionario, el algoritmo procesará tus variables para brindarte un diagnóstico proyectado y recomendaciones personalizadas.")
    
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
    
    # Uso de markdown en lugar de subheader para evitar la línea divisoria
    st.markdown(f"### Pregunta {st.session_state.paso + 1} de 8")
    st.progress((st.session_state.paso) / 8)
    
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

# --- PANTALLA DE RESULTADOS ---
else:
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    if not os.path.exists(ruta_modelo):
        st.error(f"Error: No se encuentra el archivo en {ruta_modelo}")
        st.stop()
        
    modelo = joblib.load(ruta_modelo)
    datos = np.array([st.session_state.respuestas])
    estres = modelo.predict(datos)[0]
    rendimiento = 2 - estres
    
    st.markdown("### 📋 Informe de Resultados")
    
    col1, col2 = st.columns(2)
    col1.metric("Estrés Detectado", ["BAJO", "MODERADO", "ALTO"][estres])
    col2.metric("Rendimiento", ["MALO", "IRREGULAR", "ALTO"][rendimiento])
    
    st.write("") # Espaciado
    st.info(f"💡 **Recomendación:** {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
    
    if estres == 2:
        st.warning("⚠️ **Nota de Atención Profesional:** Se recomienda considerar una consulta con el área de Bienestar Universitario para gestionar mejor estos niveles de estrés.")
    else:
        st.success("¡Excelente ritmo, continúa así!")

    if st.button("🔄 Reiniciar Evaluación"):
        st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})
        st.rerun()
