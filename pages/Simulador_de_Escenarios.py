import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Simulador de Escenarios", page_icon="🔄", layout="wide")
st.markdown("<style>.stApp { background-color: #0f1116; }</style>", unsafe_allow_html=True)

st.title("🔄 Simulador de Escenarios: Proyecciones")
st.markdown("---")

if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos_base = np.array(diag['datos']) 
    pred_base = diag['resultado']
    
    st.info("💡 Hemos cargado tu diagnóstico. Vamos a proyectar cómo cambiaría tu nivel de estrés según tus decisiones:")

    if st.button("🚀 Ejecutar Análisis Multiescenario"):
        ruta_modelo = "modelos/modelo_stress_rf.pkl"
        if not os.path.exists(ruta_modelo):
            st.error("Error: No se encontró el modelo entrenado.")
            st.stop()
            
        modelo = joblib.load(ruta_modelo)
        
        # Escenario 1: Priorizar Sueño (+3 en índice 3)
        d1 = datos_base.copy()
        d1[3] = np.clip(d1[3] + 3, 0, 10) 
        res1 = modelo.predict(d1.reshape(1, -1))[0]
        
        # Escenario 2: Reducir Ansiedad (-5 en índice 0 para notar cambio)
        d2 = datos_base.copy()
        d2[0] = np.clip(d2[0] - 5, 0, 10)
        res2 = modelo.predict(d2.reshape(1, -1))[0]
        
        # Escenario 3: Plan Integral (+2 Sueño, -3 Carga, -2 Presión)
        d3 = datos_base.copy()
        d3[3] = np.clip(d3[3] + 2, 0, 10)
        d3[5] = np.clip(d3[5] - 3, 0, 10)
        d3[7] = np.clip(d3[7] - 2, 0, 10)
        res3 = modelo.predict(d3.reshape(1, -1))[0]
        
        # Mapa de resultados
        mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
        
        st.subheader("📊 Resultados de las Proyecciones")
        col1, col2, col3 = st.columns(3)
        
        # Función auxiliar para mostrar métrica
        def mostrar_resultado(col, titulo, res, base):
            with col:
                st.write(f"**{titulo}**")
                st.metric("Resultado", mapa_label.get(res, "Desconocido"))
                if res < base: st.success("✅ Mejora significativa")
                elif res == base: st.info("ℹ️ Sin cambios")
                else: st.warning("⚠️ Efecto contraproducente")

        mostrar_resultado(col1, "Priorizar Sueño", res1, pred_base)
        mostrar_resultado(col2, "Controlar Ansiedad", res2, pred_base)
        mostrar_resultado(col3, "Plan Integral", res3, pred_base)

        st.markdown("---")
        with st.expander("Ver detalles técnicos de la predicción"):
            st.write(f"Diagnóstico Base: {mapa_label.get(pred_base)}")
            st.write(f"Datos originales: {datos_base}")
            
else:
    st.warning("⚠️ Realiza primero el diagnóstico en el 'Detector de Estrés'.")
