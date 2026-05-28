import streamlit as st
import joblib
import numpy as np
import os

st.title("🔄 Simulador de Escenarios")
st.markdown("---")

# Verificamos si hay un diagnóstico previo
if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos_base = diag['datos'] # Estos son los 10 valores que el usuario puso en el Detector
    pred_base = diag['resultado']
    
    st.info("💡 Hemos cargado tus datos del último diagnóstico. Presiona el botón para proyectar cambios.")
    
    # Mostramos resumen rápido
    st.write(f"Tu nivel de estrés detectado fue: **{pred_base}**")
    
    if st.button("Ejecutar Proyección de Escenario"):
        ruta_modelo = "modelos/modelo_stress_rf.pkl"
        modelo = joblib.load(ruta_modelo)
        
        # Simulamos un cambio (ejemplo: mejoras en sueño y reducción de ansiedad)
        datos_simulados = np.array(datos_base).copy()
        datos_simulados[3] = min(10, datos_simulados[3] + 2) # Mejora sueño
        datos_simulados[0] = max(1, datos_simulados[0] - 2)  # Reduce ansiedad
        
        nueva_pred = modelo.predict(datos_simulados.reshape(1, -1))[0]
        
        st.subheader("📊 Resultados de la Proyección")
        if nueva_pred < pred_base:
            st.success(f"¡Buenas noticias! Si logras estos cambios, tu nivel de estrés bajaría a: {nueva_pred}")
        else:
            st.warning("Los cambios sugeridos no son suficientes para reducir el nivel de estrés significativamente.")
            
else:
    st.warning("⚠️ No has realizado un diagnóstico aún.")
    st.info("Por favor, ve al 'Detector de Estrés', realiza la evaluación y luego regresa aquí para simular escenarios.")
