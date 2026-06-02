import streamlit as st
import joblib
import numpy as np
import os

# Configuración: Layout 'centered' evita que la pantalla se estire y centra el contenido
st.set_page_config(page_title="Detector Integral", layout="centered")

# Título principal
st.title("🧠 Detector Integral Académico")

# 1. Inicialización de sesión
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})

# --- PANTALLA DE BIENVENIDA (Nueva) ---
if not st.session_state.iniciado:
    st.markdown("""
    ### Bienvenido al sistema de evaluación
    Este sistema utiliza inteligencia artificial para analizar tu salud académica basada en tus estilos de vida. 
    Al completar este breve cuestionario, recibirás un diagnóstico y recomendaciones personalizadas.
    """)
    
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
    
    st.subheader(f"Pregunta {st.session_state.paso + 1} de 8")
    # Barra de progreso para darle un toque más profesional
    st.progress((st.session_state.paso) / 8)
    
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

# --- PANTALLA DE RESULTADOS ---
else:
    # 3. Predicción del modelo
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    if not os.path.exists(ruta_modelo):
        st.error(f"Error: No se encuentra el archivo en {ruta_modelo}")
        st.stop()
        
    modelo = joblib.load(ruta_modelo)
    datos = np.array([st.session_state.respuestas])
    estres = modelo.predict(datos)[0] # 0: BAJO, 1: MODERADO, 2: ALTO
    
    # 4. Lógica de rendimiento
    rendimiento = 2 - estres 
    
    # 6. Mostrar resultados visuales
    st.subheader("📋 Resultados Finales")
    
    # Usamos st.metric para que se vea más profesional y ordenado
    m1, m2 = st.columns(2)
    m1.metric("Estrés Detectado", ["BAJO", "MODERADO", "ALTO"][estres])
    m2.metric("Rendimiento", ["MALO", "IRREGULAR", "ALTO"][rendimiento])
    
    st.markdown("---")
    st.info(f"💡 Recomendación: {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
    st.info(f"💡 Análisis Académico: {['Necesitas tutorías extra.', 'Organiza mejor tus tiempos.', '¡Excelente ritmo, continúa así!'][rendimiento]}")

    # 7. Reiniciar
    if st.button("Reiniciar"):
        st.session_state.update({'paso': 0, 'respuestas': [], 'iniciado': False})
        st.rerun()
