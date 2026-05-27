import streamlit as st
import joblib
import numpy as np
import os

st.title("🔄 Simulador de Escenarios de Estilo de Vida")
st.markdown("---")

ruta_stress = "modelos/modelo_stress_rf.pkl"
ruta_burnout = "modelos/modelo_burnout_rf.pkl"

if os.path.exists(ruta_stress) and os.path.exists(ruta_burnout):
    mod_stress = joblib.load(ruta_stress)
    mod_burnout = joblib.load(ruta_burnout)
    
    col1, col2 = st.columns(2)
    with col1:
        h_sueno = st.slider("Horas de Sueño", 4, 10, 7)
        calidad_s = st.slider("Calidad de Sueño", 0, 5, 3)
        act_extra = st.slider("Actividades Extracurriculares", 0, 20, 5)
    with col2:
        carga = st.slider("Carga de Trabajo Semanal", 10, 60, 30)
        ansiedad = st.slider("Nivel de Ansiedad", 0, 21, 10)
        rendimiento = st.slider("Rendimiento Académico", 0, 5, 3)

    if st.button("Ejecutar Simulación"):
        # INTENTO DE PREDICCIÓN CON DIAGNÓSTICO
        try:
            # Creamos arrays genéricos
            # NOTA: Si da error de "features", ajusta el tamaño de estas listas
            datos_stress = np.array([[ansiedad, 5, 5, calidad_s, rendimiento, (carga/6), 5, 5, act_extra, 5]])
            datos_burnout = np.array([[h_sueno, 5, 5, rendimiento, ansiedad, 5]])
            
            pred_stress = mod_stress.predict(datos_stress)[0]
            pred_burnout = mod_burnout.predict(datos_burnout)[0]
            
            st.subheader("📊 Resultados")
            st.write(f"Estrés (Cat): {pred_stress} | Burnout (Índice): {pred_burnout:.2f}")
            
        except ValueError as e:
            st.error("Error de configuración:")
            st.code(str(e))
            st.info("Mira arriba el error: donde dice 'expecting X features', ese número X es el que debes poner en la lista de arriba.")
else:
    st.error("Modelos no encontrados en la carpeta /modelos")
