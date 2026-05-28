import streamlit as st
import joblib
import numpy as np
import os

st.title("🔄 Simulador de Escenarios: Impacto en el Estrés")
st.markdown("""
Esta herramienta permite proyectar cómo cambios en tus hábitos académicos pueden alterar tu nivel de estrés.
Ajusta las variables y observa cómo responde el sistema.
""")
st.markdown("---")

ruta_stress = "modelos/modelo_stress_rf.pkl"

if os.path.exists(ruta_stress):
    mod_stress = joblib.load(ruta_stress)
    
    col1, col2 = st.columns(2)
    with col1:
        anx = st.slider("Nivel de Ansiedad (1-10)", 1, 10, 5)
        self_e = st.slider("Autoestima (1-10)", 1, 10, 5)
        dep = st.slider("Depresión (1-10)", 1, 10, 5)
        sleep = st.slider("Calidad de Sueño (1-10)", 1, 10, 5)
        acad = st.slider("Rendimiento Académico (1-10)", 1, 10, 5)
    with col2:
        load = st.slider("Carga de Estudio (1-10)", 1, 10, 5)
        soc = st.slider("Apoyo Social (1-10)", 1, 10, 5)
        peer = st.slider("Presión de Pares (1-10)", 1, 10, 5)
        extra = st.slider("Actividades Extras (1-10)", 1, 10, 5)
        bull = st.slider("Experiencia de Bullying (1-10)", 1, 10, 5)

    if st.button("Ejecutar Simulación de Escenario"):
        datos_actuales = np.array([[anx, self_e, dep, sleep, acad, load, soc, peer, extra, bull]])
        pred_actual = mod_stress.predict(datos_actuales)[0]
        
        st.subheader("📊 Resultados de la Simulación")
        
        # Mostrar estado actual
        res_map = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
        st.info(f"**Resultado con configuración actual:** Nivel {res_map[pred_actual]}")
        
        # Simulación de Escenario Optimista (Mejorar sueño y reducir ansiedad)
        datos_opt = datos_actuales.copy()
        datos_opt[0, 3] = min(10, datos_opt[0, 3] + 2) # Mejora sueño
        datos_opt[0, 0] = max(1, datos_opt[0, 0] - 2)  # Reduce ansiedad
        
        pred_opt = mod_stress.predict(datos_opt)[0]
        
        st.write("---")
        st.subheader("🔮 Proyección de Escenario Alternativo")
        if pred_opt < pred_actual:
            st.success(f"Si optimizas tus hábitos (más sueño, menos ansiedad), tu nivel de estrés bajaría a: {res_map[pred_opt]}.")
        else:
            st.warning("Manteniendo los hábitos actuales o ante cambios leves, el nivel de estrés tiende a estabilizarse en: " + res_map[pred_opt])

else:
    st.error("Error: El modelo 'modelo_stress_rf.pkl' no fue encontrado en la carpeta /modelos.")
