import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Detector Integral Académico")

# 1. Inicializar sesión de forma robusta
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': []})

# Definición de preguntas
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

# 2. Flujo de cuestionario
if st.session_state.paso < len(preguntas):
    st.subheader(f"Pregunta {st.session_state.paso + 1} de {len(preguntas)}")
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()

else:
    # 3. Predicción del modelo
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    if not os.path.exists(ruta_modelo):
        st.error(f"Error: No se encuentra el archivo en {ruta_modelo}")
        st.stop()
        
    modelo = joblib.load(ruta_modelo)
    datos = np.array([st.session_state.respuestas])
    estres = modelo.predict(datos)[0] # 0: BAJO, 1: MODERADO, 2: ALTO
    
    # 4. Lógica de rendimiento (Consecuencia del Estrés)
    rendimiento = 2 - estres # 0: MALO, 1: IRREGULAR, 2: ALTO
    
    # 5. GUARDADO EN SESSION_STATE (Crucial para Reportes y Simulador)
    st.session_state['ultimo_diagnostico'] = {
        'datos': st.session_state.respuestas,
        'estres': estres,
        'rendimiento': rendimiento
    }
    
    # 6. Mostrar resultados
    st.subheader("📋 Resultados Finales")
    st.write(f"**Nivel de Estrés Detectado:** {['BAJO', 'MODERADO', 'ALTO'][estres]}")
    st.write(f"**Proyección de Rendimiento:** {['MALO', 'IRREGULAR', 'ALTO'][rendimiento]}")
    
    st.markdown("---")
    st.info(f"💡 Recomendación: {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
    st.info(f"💡 Análisis Académico: {['Necesitas tutorías extra.', 'Organiza mejor tus tiempos.', '¡Excelente ritmo, continúa así!'][rendimiento]}")

    # 7. Reiniciar
    if st.button("Reiniciar"):
        # Limpiar datos previos
        if 'ultimo_diagnostico' in st.session_state:
            del st.session_state['ultimo_diagnostico']
        st.session_state.update({'paso': 0, 'respuestas': []})
        st.rerun()
