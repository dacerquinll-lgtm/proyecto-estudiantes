import streamlit as st

st.set_page_config(page_title="Bienestar Estudiantil", page_icon="🎓", layout="wide")

# CSS para un look profesional
st.markdown("""
    <style>
    /* Fondo y fuentes */
    .stApp { background-color: #f4f7f6; }
    
    /* Tarjetas personalizadas */
    .css-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Botones personalizados */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #007BFF;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Sistema Inteligente de Bienestar Estudiantil")

# Header con columnas para dar aire visual
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Bienvenido a tu Centro de Analítica")
    st.write("Plataforma avanzada para el monitoreo de salud mental y rendimiento académico mediante IA.")
with col2:
    st.info("💡 **Estado del Sistema:** Operativo")

st.markdown("---")

# Módulos organizados en filas (Cards)
row1 = st.columns(3)
with row1[0]:
    st.markdown('<div class="css-card"><h4>📊 Dashboard</h4><p>Visualiza métricas generales y tendencias de datos.</p></div>', unsafe_allow_html=True)
with row1[1]:
    st.markdown('<div class="css-card"><h4>🧠 Detector</h4><p>Evalúa tus niveles de estrés en tiempo real con IA.</p></div>', unsafe_allow_html=True)
with row1[2]:
    st.markdown('<div class="css-card"><h4>🔄 Simulador</h4><p>Proyecta cambios en tu estilo de vida.</p></div>', unsafe_allow_html=True)

# Sección de estado del sistema
if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    st.success("✅ Datos cargados correctamente en el sistema.")
else:
    st.warning("⚠️ Esperando inicialización de datasets en /datasets.")
