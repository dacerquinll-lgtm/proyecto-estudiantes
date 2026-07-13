import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

pagina_activa = 2

st.markdown(f"""
    <style>
    .stApp {{
        background-color: #f8f9fa !important;
    }}
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }}
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    .header-institucional {{
        background-color: #0c1c30;
        padding: 20px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        margin-top: 0px !important;
        margin-bottom: 0px;
        border-radius: 8px 8px 0 0;
    }}
    .header-institucional h2 {{
        color: white !important;
        margin: 0;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }}
    .header-logo {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {{
        background-color: #142840 !important;
        padding: 10px 20px !important;
        margin-top: 0px !important;
        margin-bottom: 30px !important;
        border-radius: 0 0 8px 8px !important;
        gap: 0px !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="stPageLink"] a {{
        background-color: transparent !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 0.9rem !important;
        padding: 6px 12px !important;
        text-decoration: underline !important;
        box-shadow: none !important;
        display: inline-flex !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="stPageLink"] a:hover {{
        color: #cfd8dc !important;
        text-decoration: underline !important;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) > div[data-testid="column"]:nth-of-type({pagina_activa}) div[data-testid="stPageLink"] a {{
        background-color: #2e7d32 !important;
        color: white !important;
        text-decoration: none !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
    }}
    
    h1, h2, h3, h4 {{
        color: #0c1c30 !important;
        font-weight: bold !important;
    }}
    
    /* Forzar texto de métricas y títulos */
    div[data-testid="stMetric"] {{
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }}
    div[data-testid="stMetric"] label[data-testid="stMetricLabel"] p {{
        color: #4a5568 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stMetricValue"] div {{
        color: #0c1c30 !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
    }}
    
    /* Arreglo para que las pestañas (Tabs) se vean perfectamente */
    button[data-baseweb="tab"] {{
        color: #718096 !important;
        font-weight: 600 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #2e7d32 !important;
        border-bottom-color: #2e7d32 !important;
    }}
    
    div[data-testid="stNotification"] * {{
        color: #0c1c30 !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-institucional">
        <div class="header-logo">
            <span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span>
        </div>
        <div>
            <h2>Sistema Inteligente para la Reducción de Estrés en Universitarios</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

cols_nav = st.columns([1, 1.3, 1.2, 1.3, 1.4, 4])
with cols_nav[0]:
    st.page_link("app.py", label="Inicio", icon=None)
with cols_nav[1]:
    st.page_link("pages/Dashboard_General.py", label="Dashboard General", icon=None)
with cols_nav[2]:
    st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés", icon=None)
with cols_nav[3]:
    st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación", icon=None)
with cols_nav[4]:
    st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios", icon=None)

if 'datasets' not in st.session_state or st.session_state['datasets'] is None:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ Archivo no encontrado. Por favor, asegúrese de tener 'datasets/StressLevelDataset_limpio.csv'.")
        st.stop()

df = st.session_state.datasets['estres']

mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
df['stress_label'] = df['stress_level'].map(mapa_label)

st.title("📊 Centro de Analítica Estudiantil")

col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df))
col2.metric("Nivel de Estrés Promedio", mapa_label.get(int(round(df['stress_level'].mean())), "N/A"))
col3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("Evolución del Rendimiento Académico")
    
    df_line = df.groupby(['stress_level', 'stress_label'])['academic_performance'].mean().reset_index()
    df_line = df_line.sort_values('stress_level')
    
    fig1 = px.line(df_line, x="stress_label", y="academic_performance", 
                   markers=True,
                   template="plotly_white",
                   line_shape="spline",
                   labels={"stress_label": "Nivel de Estrés", 
                           "academic_performance": "Rendimiento Académico Promedio"})
    
    fig1.update_traces(line_color="#0c1c30", line_width=4, marker=dict(size=12, color="#2e7d32"))
    fig1.update_yaxes(range=[0, 5])
    
    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0c1c30"),
        xaxis=dict(
            title_font=dict(color="#0c1c30"),
            showgrid=True, 
            gridcolor="#e2e8f0", 
            linecolor="#0c1c30", 
            tickfont=dict(color="#0c1c30")
        ),
        yaxis=dict(
            title_font=dict(color="#0c1c30"),
            showgrid=True, 
            gridcolor="#e2e8f0", 
            linecolor="#0c1c30", 
            tickfont=dict(color="#0c1c30")
        )
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', 
                  color='stress_label', template="plotly_white",
                  labels={"stress_label": "Nivel de Estrés", 
                          "anxiety_level": "Nivel de Ansiedad Promedio"},
                  color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    
    fig2.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0c1c30"),
        xaxis=dict(
            title_font=dict(color="#0c1c30"),
            linecolor="#0c1c30", 
            tickfont=dict(color="#0c1c30")
        ),
        yaxis=dict(
            title_font=dict(color="#0c1c30"),
            showgrid=True, 
            gridcolor="#e2e8f0", 
            linecolor="#0c1c30", 
            tickfont=dict(color="#0c1c30")
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Interpretación:** La tendencia descendente confirma que, al aumentar el nivel de estrés, el rendimiento académico disminuye de forma consistente.")
