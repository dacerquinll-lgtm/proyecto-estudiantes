import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Reportes y Exportación", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
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
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) span {
        color: #ffffff !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) p {
        color: #ffffff !important;
    }
    
    h1, h2, h3, h4 { color: #0c1c30 !important; font-weight: bold !important; }
    
    div[data-testid="stAlert"] {
        background-color: #d4edda !important;
        border: 1px solid #c3e6cb !important;
    }
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] span {
        color: #155724 !important;
        font-weight: bold !important;
    }
    
    div[data-testid="stTextInput"] label p {
        color: #0c1c30 !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #0c1c30 !important;
        border: 1px solid #ced4da !important;
    }
    
    div.stDownloadButton > button {
        background-color: #218838 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 12px 30px !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #1e7e34 !important;
    }
    div.stDownloadButton > button p {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: bold !important;
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

st.title("📄 Generador de Reportes y Exportación")

if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos = diag['datos']
    estres = diag['estres']
    rendimiento = diag['rendimiento']
    
    mapa_estres = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
    mapa_rend = {0: "MALO", 1: "IRREGULAR", 2: "ALTO"}
    
    st.success("✅ Diagnóstico detectado. Generando PDF.")
    nombre = st.text_input("Nombre Completo del Estudiante:", "Estudiante")

    def generar_pdf(nombre, estres_txt, rend_txt, datos):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "REPORTE INTEGRAL ACADÉMICO")
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Estudiante: {nombre}")
        c.drawString(50, 700, f"Nivel de Estrés: {estres_txt}")
        c.drawString(50, 680, f"Proyección de Rendimiento: {rend_txt}")
        
        c.drawString(50, 650, "Métricas registradas:")
        y = 630
        labels = ["Ansiedad", "Autoestima", "Depresión", "Calidad de Sueño", 
                  "Carga de Estudio", "Actividades Extras", "Apoyo Social", "Interés Académico"]
        for i, label in enumerate(labels):
            c.drawString(70, y, f"- {label}: {datos[i]}")
            y -= 20
        c.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = generar_pdf(nombre, mapa_estres.get(estres), mapa_rend.get(rendimiento), datos)
    
    st.download_button(
        label="📥 Descargar Reporte (PDF)",
        data=pdf_buffer,
        file_name=f"Reporte_{nombre.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

else:
    st.warning("⚠️ No se ha detectado un diagnóstico activo.")

st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
