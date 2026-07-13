import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# CSS para la cabecera exacta de tu imagen
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    [data-testid="stHeader"] { display: none !important; }
    
    /* Contenedor oscuro de la cabecera */
    .custom-header {
        background-color: #0c1c30;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: white;
    }
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .ucv-text { color: #e53935 !important; font-weight: 900; font-size: 1.8rem; margin: 0; }
    .title-text { color: white !important; font-weight: 700; font-size: 1.4rem; margin: 0; }
    
    /* Estilo para los enlaces de navegación */
    [data-testid="stPageLink"] a {
        color: white !important;
        font-weight: bold !important;
        text-decoration: underline !important;
    }
    [data-testid="stPageLink"] a:hover { color: #cfd8dc !important; }
    </style>
""", unsafe_allow_html=True)

# Estructura de la Cabecera
st.markdown("""
    <div class="custom-header">
        <div class="header-top">
            <h1 class="ucv-text">UCV</h1>
            <h2 class="title-text">Sistema Inteligente para la Reducción de Estrés en Universitarios</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

# Fila de navegación (alineada debajo dentro del bloque oscuro)
cols = st.columns([1, 1, 1, 1, 1, 5])
with cols[0]: st.page_link("app.py", label="Inicio")
with cols[1]: st.page_link("pages/Dashboard_General.py", label="Dashboard General")
with cols[2]: st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés")
with cols[3]: st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación")
with cols[4]: st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios")

# Lógica de Datos
if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("Archivo no encontrado.")
        st.stop()

df = st.session_state.datasets['estres']
mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
df['stress_label'] = df['stress_level'].map(mapa_label)

# Dashboard
st.title("Centro de Analítica Estudiantil")

# Tarjetas de métricas (CSS corregido para fondo blanco y letras oscuras)
st.markdown("""
    <style>
    .metric-card { background: white; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; }
    .metric-label { color: #555; font-size: 0.9rem; }
    .metric-val { color: #0c1c30; font-size: 1.8rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Estudiantes</div><div class="metric-val">{len(df)}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Nivel de Estrés Promedio</div><div class="metric-val">{mapa_label.get(int(round(df["stress_level"].mean())), "N/A")}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">Ansiedad Promedio</div><div class="metric-val">{round(df["anxiety_level"].mean(), 2)}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Gráficos
t1, t2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])
with t1:
    fig1 = px.line(df.groupby(['stress_label'])['academic_performance'].mean().reset_index(), x="stress_label", y="academic_performance", markers=True, template="plotly_white")
    fig1.update_traces(line_color="#0c1c30", marker=dict(size=10, color="#2e7d32"))
    st.plotly_chart(fig1, use_container_width=True)

with t2:
    fig2 = px.bar(df.groupby(['stress_label'])['anxiety_level'].mean().reset_index(), x='stress_label', y='anxiety_level', color='stress_label', template="plotly_white", color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
