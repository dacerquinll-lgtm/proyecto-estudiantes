import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Simulador de Proyecciones", page_icon="📈", layout="wide")

st.title("📈 Simulador de Proyecciones de Bienestar")
st.markdown("---")

if 'ultimo_diagnostico' not in st.session_state:
    st.warning("⚠️ Debes completar primero el diagnóstico en el Detector Integral.")
    st.stop()

diag = st.session_state['ultimo_diagnostico']
datos_base = np.array(diag['datos']) 
estres_base = diag['estres']

st.write("Esta herramienta compara cómo evolucionaría tu situación académica según las acciones que decidas tomar.")

if st.button("🚀 Calcular Proyecciones"):
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    modelo = joblib.load(ruta_modelo)
    
    # --- ESCENARIOS ---
    # 1. Situación actual: Mantener hábitos actuales
    res_actual = estres_base
    
    # 2. Situación con cambios positivos: Mejor gestión y autocuidado
    d_mejora = datos_base.copy()
    d_mejora[3] += 2  # Sueño
    d_mejora[4] -= 2  # Carga de estudio
    d_mejora[6] += 2  # Apoyo social
    res_mejora = modelo.predict(d_mejora.reshape(1, -1))[0]
    
    # 3. Situación con más dificultades: Aumento de carga y abandono de hábitos
    d_dificultad = datos_base.copy()
    d_dificultad[4] += 3  # Aumento carga
    d_dificultad[5] -= 3  # Menos recreación
    res_dificultad = modelo.predict(d_dificultad.reshape(1, -1))[0]

    # --- PRESENTACIÓN ---
    col1, col2, col3 = st.columns(3)
    
    def render_escenario(col, titulo, res, icono, explicacion):
        rend = 2 - res
        with col:
            st.subheader(f"{icono} {titulo}")
            st.metric("Nivel de Estrés", ["Bajo", "Moderado", "Alto"][res])
            st.metric("Rendimiento", ["Malo", "Irregular", "Alto"][rend])
            st.write(f"**Análisis:** {explicacion}")

    render_escenario(col1, "Situación Actual", res_actual, "⚖️", 
                    "Es el resultado de continuar con tus hábitos de siempre. El nivel de estrés se mantendrá estable si no intervienes.")
    
    render_escenario(col2, "Si realizas mejoras", res_mejora, "✅", 
                    "Al ajustar tu descanso y reducir la sobrecarga, el modelo proyecta una baja en el estrés y un mejor rendimiento académico.")
    
    render_escenario(col3, "Si aumentan las dificultades", res_dificultad, "⚠️", 
                    "Si descuidas tus horas de sueño o aumenta tu carga académica sin apoyo, el nivel de estrés puede elevarse, afectando tu rendimiento.")

    st.markdown("---")
    st.info("💡 **Recuerda:** Estas proyecciones sirven como guía para tu toma de decisiones. Pequeños cambios en tus hábitos cotidianos tienen un impacto acumulativo real en tu salud y notas.")
