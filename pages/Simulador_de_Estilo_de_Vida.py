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
    
    st.markdown("### Ajuste las métricas para proyectar su bienestar:")
    
    col1, col2 = st.columns(2)
    with col1:
        h_sueno = st.slider("Horas de Sueño", 4, 10, 7)
        calidad_s = st.slider("Calidad de Sueño (0-5)", 0, 5, 3)
        act_extra = st.slider("Actividades Extracurriculares", 0, 20, 5)
    with col2:
        carga = st.slider("Carga de Trabajo Semanal", 10, 60, 30)
        ansiedad = st.slider("Nivel de Ansiedad (0-21)", 0, 21, 10)
        rendimiento = st.slider("Rendimiento Académico (0-5)", 0, 5, 3)

    if st.button("Ejecutar Simulación de Impacto"):
        try:
            # Arrays ajustados a las dimensiones requeridas por tus modelos
            datos_stress = np.array([[ansiedad, 5, 5, calidad_s, rendimiento, (carga/6), 5, 5, act_extra, 5]])
            datos_burnout = np.array([[h_sueno, 5, 5, rendimiento, ansiedad, 5]])
            
            pred_stress = mod_stress.predict(datos_stress)[0]
            pred_burnout = mod_burnout.predict(datos_burnout)[0]
            
            # --- INTERPRETACIÓN DE RESULTADOS ---
            st.subheader("📊 Resultados de la Proyección")
            
            # Mapeo de Estrés
            mapa_stress = {0: ("BAJO", "success"), 1: ("MODERADO", "warning"), 2: ("ALTO", "error")}
            label_s, tipo_s = mapa_stress.get(pred_stress, ("DESCONOCIDO", "info"))
            
            # Mapeo de Burnout
            if pred_burnout < 3.5:
                label_b, tipo_b = "BAJO", "success"
            elif pred_burnout <= 6.5:
                label_b, tipo_b = "MODERADO", "warning"
            else:
                label_b, tipo_b = "ALTO", "error"

            c1, c2 = st.columns(2)
            with c1:
                st.write(f"### Estrés: :{tipo_s}[{label_s}]")
                st.caption("Indica la tensión emocional proyectada bajo estas condiciones.")
            with c2:
                st.write(f"### Burnout: :{tipo_b}[{label_b} ({pred_burnout:.2f})]")
                st.caption("Escala de fatiga física y mental acumulada.")
            
            st.markdown("---")
            if tipo_s == "error" or tipo_b == "error":
                st.error("⚠️ **Alerta:** La combinación proyectada sugiere un alto riesgo de agotamiento. Se recomienda priorizar el descanso.")
            else:
                st.success("✅ **Resultado:** Las condiciones proyectadas parecen mantener un equilibrio saludable.")
                
        except Exception as e:
            st.error(f"Error técnico: {e}")
else:
    st.error("Archivos de modelos no encontrados en /modelos")
