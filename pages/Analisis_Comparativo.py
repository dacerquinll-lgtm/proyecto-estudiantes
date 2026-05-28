import streamlit as st
import plotly.express as px
import pandas as pd
import os

# 1. Configuración y Estilo Global (Para que combine con el resto)
st.set_page_config(page_title="Análisis Comparativo", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f1116; }
    h1, h2, h3 { color: #ffffff !important; }
    .stPlotlyChart { background-color: #1e1e26; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# 2. Bloque de Seguridad: Carga automática si los datos no están en sesión
if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ No se encontró el dataset. Asegúrate de que la carpeta 'datasets' existe.")
        st.stop()

# 3. Lógica de la Página
df_estres = st.session_state.datasets['estres']

st.title("📈 Análisis Comparativo y Correlaciones")
st.markdown("---")

st.markdown("### 🔍 Exploración Interactiva del Estrés Académico")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Impacto del Sueño en el Rendimiento")
    # Nota: Asegúrate que los nombres de columna coinciden exactamente con tu CSV
    fig_box = px.box(
        df_estres, x="sleep_quality", y="academic_performance", 
        color="stress_level", template="plotly_dark"
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    st.subheader("Distribución de Ansiedad por Estrés")
    fig_violin = px.violin(
        df_estres, x="stress_level", y="anxiety_level", 
        box=True, points="all", color="stress_level", template="plotly_dark"
    )
    st.plotly_chart(fig_violin, use_container_width=True)

st.markdown("---")
st.info("💡 Este análisis ahora es independiente y carga automáticamente al acceder.")
