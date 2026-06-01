import streamlit as st
import joblib
import numpy as np
import os

st.title("🧠 Detector de Rendimiento y Estrés")
st.markdown("---")

# Inicializar estados
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 0, 'respuestas': []})

# Definición de preguntas
preguntas = [
    ("¿Cuál es tu nivel de ansiedad hoy? (1-10)", 5),
    ("¿Cómo calificarías tu autoestima? (1-10)", 5),
    ("¿Qué nivel de depresión sientes? (1-10)", 5),
    ("¿Cómo es tu calidad de sueño? (1-10)", 5),
    ("¿Qué carga de estudio tienes? (1-10)", 5),
    ("¿Nivel de actividades extras? (1-10)", 5),
    ("¿Cuánto apoyo social recibes? (1-10)", 5),
    ("¿Cuál es tu interés académico actual? (1-10)", 5)
]

# Flujo de cuestionario
if st.session_state.paso < len(preguntas):
    st.subheader(f"Pregunta {st.session_state.paso + 1} de {len(preguntas)}")
    val = st.slider(preguntas[st.session_state.paso][0], 1, 10, preguntas[st.session_state.paso][1])
    
    if st.button("Siguiente"):
        st.session_state.respuestas.append(val)
        st.session_state.paso += 1
        st.rerun()
else:
    # Carga del modelo
    modelo_path = "modelos/modelo_stress_rf.pkl"
    if os.path.exists(modelo_path):
        modelo = joblib.load(modelo_path)
        datos = np.array([st.session_state.respuestas])
        
        # 1. Predicción Rendimiento (ML)
        pred_rend = modelo.predict(datos)[0]
        
        # 2. Inferencia Estrés (Lógica Clínica)
        suma_estres = st.session_state.respuestas[0] + st.session_state.respuestas[2]
        if suma_estres >= 15: estres = 2 # ALTO
        elif suma_estres >= 8: estres = 1 # MODERADO
        else: estres = 0 # BAJO

        # Resultados
        st.subheader("📋 Resultados Finales")
        
        # Estrés
        e_txt = ["BAJO", "MODERADO", "ALTO"][estres]
        st.write(f"**Nivel de Estrés Estimado:** {e_txt}")
        
        # Rendimiento
        r_txt = ["MALO", "IRREGULAR", "ALTO"][pred_rend]
        st.write(f"**Proyección de Rendimiento:** {r_txt}")
        
        st.markdown("---")
        
        # Sugerencias
        st.info(f"💡 Sugerencia Estrés: {['Mantén hábitos saludables.', 'Prioriza el descanso.', 'Busca apoyo profesional.'][estres]}")
        st.info(f"💡 Sugerencia Académica: {['Necesitas tutorías extra.', 'Organiza mejor tus tiempos.', '¡Excelente ritmo, continúa así!'][pred_rend]}")

        if st.button("Reiniciar Cuestionario"):
            st.session_state.update({'paso': 0, 'respuestas': []})
            st.rerun()
    else:
        st.error("El archivo 'modelos/modelo_stress_rf.pkl' no fue encontrado.")
