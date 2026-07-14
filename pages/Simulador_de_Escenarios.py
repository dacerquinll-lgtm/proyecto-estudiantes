import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Simulador de Proyecciones", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
    /* Fuerza el color negro en todos los textos */
    div, p, h1, h2, h3, h4, .stMetricValue, .stMetricLabel {
        color: #000000 !important;
    }
    
    .header-institucional {
        background-color: #0c1c30;
        padding: 20px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        border-radius: 8px 8px 0 0;
    }
    .header-institucional h2 { color: white !important; margin: 0; font-size: 1.2rem !important; font-weight: 600 !important; }
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        background-color: #1a2a40 !important;
        padding: 10px 20px !important;
        margin-bottom: 30px !important;
        border-radius: 0 0 8px 8px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) a {
        color: #ffffff !important; font-weight: bold !important; text-decoration: none !important;
    }
    
    /* Diseño del botón personalizado */
    div.stButton > button {
        background-color: #0c1c30 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 10px 24px !important;
    }
    div.stButton > button:hover {
        background-color: #1a2a40 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-institucional">
        <div><span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span></div>
        <div><h2>Sistema Inteligente para la Reducción de Estrés en Universitarios</h2></div>
    </div>
""", unsafe_allow_html=True)

cols_nav = st.columns([0.8, 1.2, 1.2, 1.4, 1.4])
with cols_nav[0]: st.page_link("app.py", label="Inicio")
with cols_nav[1]: st.page_link("pages/Dashboard_General.py", label="Dashboard General")
with cols_nav[2]: st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés")
with cols_nav[3]: st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación")
with cols_nav[4]: st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios")

st.title("📈 Simulador de Proyecciones de Bienestar")

if 'ultimo_diagnostico' not in st.session_state:
    st.warning("⚠️ Debes completar primero el diagnóstico en el Detector Integral.")
    st.stop()

diag = st.session_state['ultimo_diagnostico']
datos_base = np.array(diag['datos']) 
estres_base = diag['estres']

st.write("Esta herramienta compara cómo evolucionaría tu situación académica según las acciones que decidas tomar.")

if st.button("🚀 Calcular Proyecciones"):
    # Asegúrate de que la ruta sea correcta según tu estructura de carpetas
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    modelo = joblib.load(ruta_modelo)
    
    res_actual = estres_base
    
    d_mejora = datos_base.copy()
    d_mejora[3] += 2 
    d_mejora[4] -= 2 
    d_mejora[6] += 2 
    res_mejora = modelo.predict(d_mejora.reshape(1, -1))[0]
    
    d_dificultad = datos_base.copy()
    d_dificultad[4] += 3
    d_dificultad[5] -= 3
    res_dificultad = modelo.predict(d_dificultad.reshape(1, -1))[0]

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
