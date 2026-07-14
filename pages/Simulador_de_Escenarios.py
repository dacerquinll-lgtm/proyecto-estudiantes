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
    
    .texto-negro, .texto-negro p, .texto-negro div, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
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
    div[data-testid="stPageLink"] * { color: #ffffff !important; }
    
    h1, h2, h3, h4 { color: #0c1c30 !important; font-weight: bold !important; }
    
    div.stButton > button {
        background-color: #218838 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 12px 30px !important;
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

if 'calculado' not in st.session_state:
    st.session_state['calculado'] = False

diag = st.session_state['ultimo_diagnostico']
datos_base = np.array(diag['datos']) 
estres_base = diag['estres']

if not st.session_state['calculado']:
    st.markdown('<div class="texto-negro"><p style="font-size: 1.1rem; margin-bottom: 25px;">Esta herramienta compara cómo evolucionaría tu nivel de estrés según las acciones que decidas tomar.</p></div>', unsafe_allow_html=True)
    if st.button("🚀 Calcular Proyecciones"):
        st.session_state['calculado'] = True
        st.rerun()
else:
    ruta_modelo = os.path.join("modelos", "modelo_stress_rf.pkl")
    modelo = joblib.load(ruta_modelo)
    
    # Lógica corregida con factores de impacto más fuertes
    d_mejora = datos_base.copy()
    d_mejora[3] -= 3; d_mejora[4] += 4; d_mejora[6] += 4
    res_mejora = int(modelo.predict(d_mejora.reshape(1, -1))[0])
    
    d_dificultad = datos_base.copy()
    d_dificultad[3] += 5; d_dificultad[4] -= 4
    res_dificultad = int(modelo.predict(d_dificultad.reshape(1, -1))[0])

    st.markdown('<div class="texto-negro">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    def render_escenario(col, titulo, res, icono, explicacion):
        niveles = ["Bajo", "Moderado", "Alto"]
        with col:
            st.subheader(f"{icono} {titulo}")
            st.metric("Nivel de Estrés", niveles[res])
            st.markdown(f'<p style="margin-top: 10px;"><strong>Análisis:</strong> {explicacion}</p>', unsafe_allow_html=True)

    render_escenario(col1, "Situación Actual", estres_base, "⚖️", "Tu nivel actual según tus hábitos registrados.")
    render_escenario(col2, "Si realizas mejoras", res_mejora, "✅", "Al reducir la carga y mejorar hábitos, el modelo proyecta una disminución del estrés.")
    render_escenario(col3, "Si aumentan dificultades", res_dificultad, "⚠️", "La sobrecarga académica intensa eleva el riesgo de un estrés alto.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("⬅️ Volver al Simulador"):
        st.session_state['calculado'] = False
        st.rerun()

    st.info("💡 **Recuerda:** Estas proyecciones sirven como guía para tu toma de decisiones.")
