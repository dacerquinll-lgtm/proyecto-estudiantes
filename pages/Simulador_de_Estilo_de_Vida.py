import streamlit as st
import joblib
import numpy as np
import os

st.title("🔄 Simulador de Escenarios de Estilo de Vida")
st.markdown("---")

# Rutas a los modelos
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_stress = os.path.join(base_dir, "modelos", "modelo_stress_rf.pkl")
ruta_burnout = os.path.join(base_dir, "modelos", "modelo_burnout_rf.pkl")

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
            # Preparación de datos según la estructura de entrenamiento de tus modelos
            datos_stress = np.array([[ansiedad, 5, 5, calidad_s, rendimiento, (carga/6), 5, 5, act_extra, 5]])
            datos_burnout = np.array([[h_sueno, 5, 5, rendimiento, ansiedad, 5]])
            
            # Predicciones
            pred_stress = mod_stress.predict(datos_stress)[0]
            pred_burnout = mod_burnout.predict(datos_burnout)[0]
            
            st.subheader("📊 Resultados de la Proyección")
            
            # Visualización Estrés
            st.write("#### 🧠 Nivel de Estrés Estimado:")
            if pred_stress == 0:
                st.success("BAJO: Tu nivel de tensión es saludable y manejable.")
            elif pred_stress == 1:
                st.warning("MODERADO: Presentas signos de estrés que requieren mayor organización.")
            else:
                st.error("ALTO: Tus niveles de estrés son preocupantes. Evalúa reducir tu carga.")
            
            # Visualización Burnout
            st.write("#### 📉 Índice de Burnout Proyectado:")
            if pred_burnout < 3.5:
                st.success(f"BAJO ({pred_burnout:.2f}): Estado de bienestar óptimo.")
            elif pred_burnout <= 6.5:
                st.warning(f"MODERADO ({pred_burnout:.2f}): Existe riesgo de fatiga mental acumulada.")
            else:
                st.error(f"ALTO ({pred_burnout:.2f}): Riesgo crítico de agotamiento. Busca soporte.")
                
        except Exception as e:
            st.error(f"Error técnico durante la simulación: {e}")
else:
    st.error("Archivos de modelos no encontrados en la carpeta /modelos. Verifica la ruta.")
