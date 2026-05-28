import streamlit as st
import joblib
import numpy as np
import os

st.title("🔄 Simulador de Escenarios")

if 'datos_usuario' in st.session_state:
    d = st.session_state['datos_usuario']
    st.info("✅ Se han cargado tus últimos datos automáticamente.")
else:
    d = [5] * 10
    st.warning("No hay datos previos, usando valores por defecto.")

# Sliders usando los valores de 'd'
col1, col2 = st.columns(2)
with col1:
    anx = st.slider("Ansiedad", 1, 10, d[0])
    # ... (restante de sliders igual que arriba) ...
    
if st.button("Ejecutar Simulación"):
    # Aquí procesas la simulación con los valores actuales de los sliders
    st.success("Simulación ejecutada con éxito.")
