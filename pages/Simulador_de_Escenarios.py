import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Simulador Proyectivo", page_icon="📈", layout="wide")

st.title("📈 Simulador Proyectivo de Bienestar")
st.markdown("---")

if 'ultimo_diagnostico' not in st.session_state:
    st.warning("⚠️ Debes completar primero el diagnóstico en el Detector Integral.")
    st.stop()

diag = st.session_state['ultimo_diagnostico']
datos_base = np.array(diag['datos']) 
estres_base = diag['estres']

st.markdown("""
Esta herramienta proyecta la evolución de tu bienestar académico basándose en tu perfil actual. 
Selecciona un escenario para visualizar la trayectoria de tu rendimiento.
""")

if st.button("🚀 Calcular Proyecciones Académicas"):
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    modelo = joblib.load(ruta_modelo)
    
    # --- DEFINICIÓN DE ESCENARIOS ---
    # Inercia: Mantener hábitos actuales
    res_inercia = estres_base
    
    # Intervención: Mejora en gestión de tiempo y autocuidado
    d_cambio = datos_base.copy()
    d_cambio[3] += 2  # Sueño
    d_cambio[4] -= 2  # Carga de estudio
    d_cambio[6] += 2  # Apoyo social
    res_cambio = modelo.predict(d_cambio.reshape(1, -1))[0]
    
    # Crisis: Aumento de carga y abandono de hábitos
    d_crisis = datos_base.copy()
    d_crisis[4] += 3  # Aumento carga
    d_crisis[5] -= 3  # Menos recreación
    res_crisis = modelo.predict(d_crisis.reshape(1, -1))[0]

    # --- PRESENTACIÓN PROFESIONAL ---
    col1, col2, col3 = st.columns(3)
    
    def render_scenario(col, title, res, icon, explanation):
        rend = 2 - res
        with col:
            st.subheader(f"{icon} {title}")
            st.metric("Estrés Proyectado", ["Bajo", "Moderado", "Alto"][res])
            st.metric("Impacto Académico", ["Crítico", "Irregular", "Alto"][rend])
            st.write(f"**Análisis:** {explanation}")

    render_scenario(col1, "Escenario Inercial", res_inercia, "⚖️", 
                    "Continuar con el ritmo actual. Existe un riesgo de estancamiento si no se introducen ajustes en la gestión de estresores.")
    
    render_scenario(col2, "Escenario de Optimización", res_cambio, "✅", 
                    "Aplicar protocolos de autocuidado y gestión de carga. Proyecta una mejora en la capacidad cognitiva y resiliencia emocional.")
    
    render_scenario(col3, "Escenario Crítico", res_crisis, "⚠️", 
                    "Incremento de carga y aislamiento. Este escenario correlaciona con un riesgo alto de agotamiento (burnout) académico.")

    st.markdown("---")
    st.info("""
    **Nota de interpretación:** Estas proyecciones son modelos matemáticos basados en tus inputs. 
    Un cambio en tus variables (Sueño, Carga, Apoyo) no garantiza el resultado, pero modifica estadísticamente la probabilidad de éxito académico.
    """)
