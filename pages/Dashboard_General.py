import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

pagina_activa = 2

st.markdown(f"""
    <style>
    .stApp {{ background-color: #f8f9fa !important; }}
    [data-testid="stHeader"], [data-testid="stSidebar"] {{ display: none !important; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    .header-institucional {{
        background-color: #0c1c30; padding: 20px 30px; display: flex; 
        align-items: center; justify-content: space-between; color: white;
        border-radius: 8px 8px 0 0;
    }}
    
    .metric-card {{
        background-color: white; padding: 20px; border-radius: 10px;
        border-left: 5px solid #0c1c30; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .metric-label {{ color: #4a5568 !important; font-size: 0.9rem !important; font-weight: bold !important; margin-bottom: 5px !important; }}
    .metric-value {{ color: #0c1c30 !important; font-size: 2rem !important; font-weight: 800 !important; }}
    
    h1, h2, h3, h4 {{ color: #0c1c30 !important; font-weight: bold !important; }}
    
    button[data-baseweb="tab"] {{ background-color: transparent !important; }}
    button[data-baseweb="tab"] div, button[data-baseweb="tab"] p {{ color: #4a5568 !important; font-weight: bold !important; font-size: 0.95rem !important; }}
    button[data-baseweb="tab"][aria-selected="true"] div, button[data-baseweb="tab"][aria-selected="true"] p {{ color: #2e7d32 !important; }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-institucional">
        <span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span>
        <h2>Sistema Inteligente para la Reducción de Estrés en Universitarios</h2>
    </div>
""", unsafe_allow_html=True)

cols_nav = st.columns([1, 1.3, 1.2, 1.3, 1.4, 4])
with cols_nav[0]: st.page_link("app.py", label="Inicio", icon=None)
with cols_nav[1]: st.page_link("pages/Dashboard_General.py", label="Dashboard General", icon=None)
with cols_nav[2]: st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés", icon=None)
with cols_nav[3]: st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación", icon=None)
with cols_nav[4]: st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios", icon=None)

if 'datasets' not in st.session_state or st.session_state['datasets'] is None:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ Archivo no encontrado.")
        st.stop()

df = st.session_state.datasets['estres']
mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
df['stress_label'] = df['stress_level'].map(mapa_label)

st.title("📊 Centro de Analítica Estudiantil")

col1, col2, col3 = st.columns(3)
with col1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Estudiantes</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-card"><div class="metric-label">Nivel de Estrés Promedio</div><div class="metric-value">{mapa_label.get(int(round(df["stress_level"].mean())), "N/A")}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-card"><div class="metric-label">Ansiedad Promedio</div><div class="metric-value">{round(df["anxiety_level"].mean(), 2)}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("Evolución del Rendimiento Académico")
    df_line = df.groupby(['stress_level', 'stress_label'])['academic_performance'].mean().reset_index().sort_values('stress_level')
    fig1 = px.line(df_line, x="stress_label", y="academic_performance", markers=True, template="plotly_white", line_shape="spline")
    fig1.update_traces(line_color="#0c1c30", line_width=4, marker=dict(size=12, color="#2e7d32"))
    fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0c1c30"))
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', color='stress_label', template="plotly_white", color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    fig2.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0c1c30"))
    st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Interpretación:** La tendencia descendente confirma que, al aumentar el nivel de estrés, el rendimiento académico disminuye de forma consistente.")
