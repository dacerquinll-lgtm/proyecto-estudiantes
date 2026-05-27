import streamlit as st
import joblib
import os
import numpy as np

st.title("🧠 Detector de Niveles de Estrés Analítico")
st.markdown("---")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_modelo = os.path.join(base_dir, "modelos", "modelo_stress_rf.pkl")

if os.path.exists(ruta_modelo):
    try:
        modelo = joblib.load(ruta_modelo)
        st.success("Modelo Predictivo Random Forest acoplado correctamente.")
        
        st.markdown("### Ingrese los parámetros de evaluación:")
        val1 = st.slider("Calidad de Sueño (0-5):", 0, 5, 3)
        val2 = st.slider("Horas de Estudio Diarias:", 1, 12, 6)
        
        if st.button("Calcular Diagnóstico"):
            prediccion = modelo.predict(np.array([[val1, val2]])) if hasattr(modelo, 'predict') else [0]
            st.metric(label="Nivel de Estrés Predicho", value=f"Nivel {prediccion[0]}")
    except Exception as e:
        st.error(f"Error al ejecutar el modelo predictivo: {e}")
else:
    st.warning(f"Archivo de modelo predictivo no detectado en: {ruta_modelo}")
