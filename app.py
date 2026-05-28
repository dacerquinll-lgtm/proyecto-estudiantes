import streamlit as st

# Configuración inicial de página
st.set_page_config(page_title="MindCare Analytics", page_icon="🧠", layout="wide")

# CSS Avanzado para romper el look estándar de Streamlit
st.markdown("""
    <style>
    /* Fondo estilo Dashboard */
    .stApp { background-color: #0f1116; }
    
    /* Tarjetas con efecto glassmorphism */
    .metric-card {
        background: linear-gradient(135deg, #1e1e26 0%, #252530 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #333;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        color: white;
    }
    
    /* Títulos personalizados */
    h1 { color: #ffffff !important; font-weight: 800 !important; }
    h3 { color: #00d4ff !important; }
    
    /* Botones estilo Neumorfismo */
    div.stButton > button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        border: none;
        color: white;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

# Título con estilo
st.title("🧠 MindCare Analytics")
st.subheader("Sistema Inteligente de Bienestar Estudiantil")

# Layout de bienvenida (Bento Box Design)
col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("""
    <div class="metric-card">
        <h3>Bienvenido de nuevo</h3>
        <p>Tu sistema está analizando datos en tiempo real. Selecciona un módulo en el menú lateral para comenzar tu sesión de trabajo.</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.info("✅ **Conexión con el Modelo:** RF-Optimizado v2.4")
    st.info("✅ **Estado de Datos:** Dataset Cargado")

# Dashboard breve de acceso rápido
st.markdown("---")
st.write("### Acceso Rápido")
quick_links = st.columns(4)

if quick_links[0].button("📊 Dashboard"): st.rerun()
if quick_links[1].button("🧠 Detector"): st.rerun()
if quick_links[2].button("🔄 Simulador"): st.rerun()
if quick_links[3].button("📄 Reportes"): st.rerun()
