import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 0rem !important; }
    
    .header-institucional {
        background-color: #0c1c30; padding: 20px 30px; display: flex; 
        align-items: center; justify-content: space-between; color: white;
        border-radius: 8px; margin-bottom: 20px;
    }
    
    .metric-card {
        background-color: white; padding: 20px; border-radius: 8px;
        border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-label { color: #64748b !important; font-size: 0.9rem !important; font-weight: 600 !important; }
    .metric-value { color: #0c1c30 !important; font-size: 1.8rem !important; font-weight: 800 !important; margin-top: 5px; }
    
    h1, h2 { color: #0c1c30 !important; font-weight: bold !important; }
    
    button[data-baseweb="tab"] { background-color: transparent !important; }
    button[data-baseweb="tab"] div { color: #64748b !important; font-weight: bold !important; }
    button[data-baseweb="tab"][aria-selected="true"] div { color: #0c1c30 !important; border-bottom: 2px solid #0c1c30; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-institucional">
        <span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span>
        <span>Sistema Inteligente para la Reducción de Estrés en Universitarios</span>
    </div>
""", unsafe_allow_html=True)

if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}

df = st.session_state.datasets['estres']
mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
df['stress_label'] = df['stress_level'].map(mapa_label)

st.title("📊 Centro de Analítica Estudiantil")

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Estudiantes</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Nivel de Estrés Promedio</div><div class="metric-value">{mapa_label.get(int(round(df["stress_level"].mean())), "N/A")}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">Ansiedad Promedio</div><div class="metric-value">{round(df["anxiety_level"].mean(), 2)}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

t1, t2 = st.tabs(["📉 Tendencia de Rendimiento", "⚠️ Factores de Riesgo"])

with t1:
    fig1 = px.line(df.groupby(['stress_label'])['academic_performance'].mean().reset_index(), x="stress_label", y="academic_performance", markers=True, template="plotly_white")
    fig1.update_traces(line_color="#0c1c30", marker=dict(size=10, color="#2e7d32"))
    st.plotly_chart(fig1, use_container_width=True)

with t2:
    fig2 = px.bar(df.groupby(['stress_label'])['anxiety_level'].mean().reset_index(), x='stress_label', y='anxiety_level', color='stress_label', template="plotly_white", color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
