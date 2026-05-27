import streamlit as st
import joblib
import numpy as np
import os

st.title("🌱 Motor de Recomendaciones")

# Ruta al modelo
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_modelo = os.path.join(base_dir, "modelos", "modelo_burnout_rf.pkl")

if os.path.exists(ruta_modelo):
    model = joblib.load(ruta_modelo)
    
    # --- AQUÍ ESTÁ EL DIAGNÓSTICO ---
    # Mostramos cuántas columnas espera el modelo
    n_features_esperadas = model.n_features_in_
    st.info(f"El modelo espera exactamente {n_features_esperadas} variables.")
    
    st.markdown("### Ingresa los datos:")
    # Creamos un formulario dinámico que suma 7 variables, 
    # si el modelo espera un número diferente, ajusta este array abajo
    val1 = st.slider("Sleep", 1, 10, 5)
    val2 = st.slider("Physical", 1, 10, 5)
    val3 = st.slider("Social", 1, 10, 5)
    val4 = st.slider("Academic", 1, 10, 5)
    val5 = st.slider("Anxiety", 1, 10, 5)
    val6 = st.slider("Depres", 1, 10, 5)
    val7 = st.slider("Lifestyle", 1, 10, 5)

    if st.button("Generar Evaluación"):
        # Ajusta este array para que tenga exactamente 'n_features_esperadas' elementos
        caracteristicas = np.array([[val1, val2, val3, val4, val5, val6, val7]])
        
        try:
            pred = model.predict(caracteristicas)
            st.success(f"Resultado: {pred[0]}")
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.write("Ajusta la cantidad de sliders para que coincidan con el número que muestra el recuadro azul arriba.")

else:
    st.error("Archivo de modelo no encontrado.")
