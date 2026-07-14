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
    .block-container {{ padding-top: 0rem !important; padding-bottom: 0rem !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    
    .header-institucional {{ background-color: #0c1c30; padding: 20px 30px; display: flex; align-items: center; justify-content: space-between; color: white; border-radius: 8px 8px 0 0; }}
    .header-institucional h2 {{ color: white !important; margin: 0; font-size: 1.2rem !important; font-weight: 600 !important; }}
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {{ background-color: #142840 !important; padding: 10px 20px !important; margin-bottom: 30px !important; border-radius: 0 0 8px 8px !important; }}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="stPageLink"] a {{ color: #ffffff !important; font-weight: bold !important; text-decoration: underline !important; }}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) > div[data-testid="column"]:nth-of-type({pagina_activa}) div[data-testid="stPageLink"] a {{ background-color: #2e7d32 !important; text-decoration: none !important; }}
    
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{ color: #0c1c30 !important; }}
    
    /* CORRECCIÓN TABS: Color oscuro para mejor contraste */
    button[data-baseweb="tab"] div {{ color: #0c1c30 !important; font-weight: bold !important; }}
    button[data-baseweb="tab"][aria-selected="true"] div {{ color: #2e7d32 !important; }}
    
    div[data-testid="stNotification"] * {{ color: #0c1c30 !important; }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-institucional">
        <div class="header-logo"><span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span></div>
        <div><h2>Sistema Inteligente para la Reducción de Estrés en Universitarios</h2></div>
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
df['stress_label'] = df['stress_level'].map({0: "BAJO", 1: "MODERADO", 2: "ALTO"})

st.title("📊 Centro de Analítica Estudiantil")
c1, c2, c3 = st.columns(3)
c1.metric("Total Estudiantes", len(df))
c2.metric("Nivel de Estrés Promedio", df['stress_label'].iloc[int(round(df['stress_level'].mean()))])
c3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

tab1, tab2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

def conf_grafico(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0c1c30", size=14),
        xaxis=dict(showgrid=False, tickfont=dict(color="#0c1c30", size=14, weight="bold")),
        yaxis=dict(showgrid=True, gridcolor="#d1d5db", tickfont=dict(color="#0c1c30", size=14, weight="bold"))
    )
    return fig

with tab1:
    df_line = df.groupby(['stress_level', 'stress_label'])['academic_performance'].mean().reset_index().sort_values('stress_level')
    fig1 = px.line(df_line, x="stress_label", y="academic_performance", markers=True)
    fig1.update_traces(line_color="#0c1c30", line_width=3, marker=dict(size=12, color="#2e7d32"))
    st.plotly_chart(conf_grafico(fig1), use_container_width=True)

with tab2:
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', color='stress_label', color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    st.plotly_chart(conf_grafico(fig2), use_container_width=True)

st.info("💡 **Interpretación:** La tendencia descendente confirma que, al aumentar el nivel de estrés, el rendimiento académico disminuye de forma consistente.")
