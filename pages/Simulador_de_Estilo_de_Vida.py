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
    
    st.markdown("### Modifique las métricas para simular el impacto en su bienestar académico:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛌 Hábitos de Descanso y Rutina")
        horas_sueno_sim = st.slider("Horas de Sueño Proyectadas (Diarias)", 4, 10, 7)
        calidad_sueno_sim = st.slider("Calidad del Sueño Esperada (0 a 5)", 0, 5, 3)
        act_extra_sim = st.slider("Horas Semanales en Actividades Extracurriculares (Simuladas)", 0, 20, 5)
        
    with col2:
        st.markdown("#### 📚 Entorno y Exigencia Académica")
        carga_semanal_sim = st.slider("Carga de Trabajo/Estudio Semanal Proyectada (Horas)", 10, 60, 30)
        ansiedad_sim = st.slider("Nivel de Ansiedad Controlado (0 a 21)", 0, 21, 10)
        rendimiento_sim = st.slider("Rendimiento Académico Objetivo (0 a 5)", 0, 5, 3)

    st.markdown("---")
    
    if st.button("Ejecutar Simulación de Impacto"):
        datos_stress = np.array([[
            ansiedad_sim, 0, 2, calidad_sueno_sim,
            rendimiento_sim, 3, 2, 3
        ]])
        
        pred_stress = mod_stress.predict(datos_stress)[0]
        
        nivel_stress_mapeado = 2 if pred_stress == 0 else (5 if pred_stress == 1 else 8)
        
        datos_burnout = np.array([[
            7.5, nivel_stress_mapeado, horas_sueno_sim, carga_semanal_sim,
            3, act_extra_sim, 0, 0
        ]])
        
        pred_burnout = mod_burnout.predict(datos_burnout)[0]
        
        st.subheader("📊 Resultados de la Proyección Simulada")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.metric(
                label="Impacto Estimado en Estrés", 
                value="BAJO" if pred_stress == 0 else ("MEDIO" if pred_stress == 1 else "ALTO")
            )
            
        with c2:
            st.metric(
                label="Índice de Burnout Proyectado", 
                value=f"{pred_burnout:.2f}"
            )
            
        st.markdown("---")
        if pred_stress == 2 or pred_burnout > 7.0:
            st.error("🚨 La combinación de variables seleccionada proyecta un riesgo crítico para tu salud mental. Intenta balancear las horas de descanso o reducir la carga horaria.")
        else:
            st.success("✅ Este escenario plantea un equilibrio saludable y sostenible a largo plazo para tu rendimiento estudiantil.")
else:
    st.error("Asegúrese de contar con ambos archivos binarios ('modelo_stress_rf.pkl' y 'modelo_burnout_rf.pkl') en la carpeta /modelos.")