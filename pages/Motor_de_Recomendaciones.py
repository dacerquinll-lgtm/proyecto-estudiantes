import streamlit as st
import joblib
import numpy as np
import os

st.title("🌱 Motor de Recomendaciones y Evaluación de Burnout")
st.markdown("---")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_modelo = os.path.join(base_dir, "modelos", "modelo_burnout_rf.pkl")

if os.path.exists(ruta_modelo):
    model = joblib.load(ruta_modelo)
    
    st.markdown("### Responda las preguntas (6 parámetros):")
    
    col1, col2 = st.columns(2)
    
    # He dejado solo 6 sliders para coincidir con las 6 variables del modelo
    with col1:
        val1 = st.slider("Sueño (sleep)", 1, 10, 7)
        val2 = st.slider("Físico (physical)", 1, 10, 5)
        val3 = st.slider("Social (social)", 1, 10, 5)
    with col2:
        val4 = st.slider("Académico (academic)", 1, 10, 5)
        val5 = st.slider("Ansiedad (anxiety)", 1, 10, 5)
        val6 = st.slider("Depresión (depres)", 1, 10, 5)
    
    if st.button("Generar Evaluación"):
        # Enviamos exactamente 6 variables
        caracteristicas = np.array([[val1, val2, val3, val4, val5, val6]])
        
        try:
            pred = model.predict(caracteristicas)
            st.success(f"Índice de Burnout Predicho: {pred[0]:.2f}")
        except Exception as e:
            st.error(f"Aún hay un desajuste: {e}")
else:
    st.error("Modelo no encontrado.")
