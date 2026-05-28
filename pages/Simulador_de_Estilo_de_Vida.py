import streamlit as st
import joblib
import numpy as np
import os

st.title("🔄 Simulador de Escenarios: Proyecciones")
st.markdown("---")

if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos_base = np.array(diag['datos']) # Tu vector de 10 variables
    pred_base = diag['resultado']
    
    st.info("💡 Hemos cargado tu diagnóstico. Vamos a proyectar cómo cambiaría tu nivel de estrés según tus decisiones:")

    if st.button("🚀 Ejecutar Análisis Multiescenario"):
        ruta_modelo = "modelos/modelo_stress_rf.pkl"
        modelo = joblib.load(ruta_modelo)
        
        # Escenario 1: Mejorar Sueño (+3 puntos en calidad)
        d1 = datos_base.copy()
        d1[3] = min(10, d1[3] + 3)
        res1 = modelo.predict(d1.reshape(1, -1))[0]
        
        # Escenario 2: Reducir Ansiedad (-3 puntos)
        d2 = datos_base.copy()
        d2[0] = max(1, d2[0] - 3)
        res2 = modelo.predict(d2.reshape(1, -1))[0]
        
        # Escenario 3: Combinado (Sueño + Carga de estudio -2)
        d3 = datos_base.copy()
        d3[3] = min(10, d3[3] + 2)
        d3[5] = max(1, d3[5] - 2)
        res3 = modelo.predict(d3.reshape(1, -1))[0]
        
        st.subheader("📊 Resultados de las Proyecciones")
        
        # Crear columnas para comparar
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Escenario: Priorizar Sueño**")
            st.metric("Resultado", f"Nivel {res1}")
            if res1 < pred_base: st.success("✅ Mejora significativa")
            else: st.warning("⚠️ Efecto leve")
            
        with col2:
            st.write("**Escenario: Controlar Ansiedad**")
            st.metric("Resultado", f"Nivel {res2}")
            if res2 < pred_base: st.success("✅ Mejora significativa")
            else: st.warning("⚠️ Efecto leve")
            
        with col3:
            st.write("**Escenario: Plan Integral**")
            st.metric("Resultado", f"Nivel {res3}")
            if res3 < pred_base: st.success("✅ Mejora efectiva")
            else: st.warning("⚠️ Efecto leve")

        st.markdown("---")
        st.write("Interpretación: Los resultados muestran cómo cambios específicos en tus hábitos afectan matemáticamente tu predisposición al estrés académico.")
            
else:
    st.warning("⚠️ Realiza primero el diagnóstico en el 'Detector de Estrés'.")
