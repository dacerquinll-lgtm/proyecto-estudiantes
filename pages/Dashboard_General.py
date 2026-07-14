import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

pagina_activa = 2

st.markdown(f"""
    <style>
    .stApp {{ background-color: #f8f9fa !important; }}
    [data-testid="stHeader"] {{ display: none !important; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    .header-institucional {{ background-color: #0c1c30; padding: 20px; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; }}
    h1, h2, h3 {{ color: #0c1c30 !important; }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-institucional">
        <div><span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span> 
        <span style="font-size: 1.2rem; font-weight: 600;">Sistema Inteligente para la Reducción de Estrés en Universitarios</span></div>
    </div>
""", unsafe_allow_html=True)

cols_nav = st.columns([1, 1.3, 1.2, 1.3, 1.4, 4])
with cols_nav[0]: st.page_link("app.py", label="Inicio")
with cols_nav[1]: st.page_link("pages/Dashboard_General.py", label="Dashboard General")
with cols_nav[2]: st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés")
with cols_nav[3]: st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación")
with cols_nav[4]: st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios")

if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta): st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else: st.stop()

df = st.session_state.datasets['estres']
mapa_niveles = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
df['stress_label'] = df['stress_level'].map(mapa_niveles)

st.title("📊 Centro de Analítica Estudiantil")

promedio_num = int(round(df['stress_level'].mean()))
nivel_promedio = mapa_niveles.get(promedio_num, "N/A")

c1, c2, c3 = st.columns(3)
c1.metric("Total Estudiantes", len(df))
c2.metric("Nivel de Estrés Promedio", nivel_promedio)
c3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

tab1, tab2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("Evolución del Rendimiento Académico")
    df_line = df.groupby(['stress_level', 'stress_label'])['academic_performance'].mean().reset_index()
    fig1 = px.line(df_line, x="stress_label", y="academic_performance", markers=True)
    fig1.update_traces(line_color="#0c1c30", marker=dict(size=12, color="#2e7d32"))
    fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0c1c30"), 
                       xaxis_title="Nivel de Estrés", yaxis_title="Rendimiento Académico")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', color='stress_label', 
                  color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0c1c30"),
                       xaxis_title="Nivel de Estrés", yaxis_title="Nivel de Ansiedad", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
