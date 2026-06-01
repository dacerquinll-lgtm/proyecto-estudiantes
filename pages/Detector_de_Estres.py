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
    ("¿Cuál es tu nivel de ansiedad actual? (1=Extrema, 10=Ninguna)", 5),
    ("¿Qué nivel de confianza tienes en ti mismo/a? (1=Muy baja, 10=Muy alta)", 5),
    ("¿Cómo calificarías tu estado de ánimo general? (1=Muy decaído, 10=Muy optimista)", 5),
    ("¿Cómo es la calidad de tu sueño? (1=Muy mala, 10=Excelente)", 5),
    ("¿Qué capacidad tienes para manejar tu carga de estudio? (1=Desbordado/a, 10=Control total)", 5),
    ("¿Qué tanto tiempo dedicas a actividades recreativas? (1=Nada, 10=Lo suficiente)", 5),
    ("¿Cuánto apoyo social sientes que recibes? (1=Nada, 10=Muchísimo)", 5),
    ("¿Cómo es tu rendimiento académico reciente? (1=Muy bajo, 10=Excelente)", 5)
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
