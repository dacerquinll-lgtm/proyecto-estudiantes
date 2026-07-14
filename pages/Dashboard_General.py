import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="MindCare Analytics - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# Mantengo tu CSS necesario para el layout, pero sin tocar colores de Plotly
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .header-institucional { background-color: #0c1c30; padding: 20px; color: white; border-radius: 8px; }
    h1, h2, h3 { color: #0c1c30 !important; }
    </style>
""", unsafe_allow_html=True)

# Carga de datos
if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}

df = st.session_state.datasets['estres']
df['stress_label'] = df['stress_level'].map({0: "BAJO", 1: "MODERADO", 2: "ALTO"})

st.title("📊 Centro de Analítica Estudiantil")

# Gráficos con configuración explícita de colores para que se vean las etiquetas
with st.container():
    st.subheader("Evolución del Rendimiento Académico")
    df_line = df.groupby(['stress_level', 'stress_label'])['academic_performance'].mean().reset_index()
    
    fig1 = px.line(df_line, x="stress_label", y="academic_performance", markers=True)
    fig1.update_traces(line_color="#0c1c30", marker=dict(size=12, color="#2e7d32"))
    
    # Aquí configuramos el color de los ejes y títulos para que sean visibles
    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0c1c30"),
        xaxis_title="Nivel de Estrés",
        yaxis_title="Rendimiento Académico",
        xaxis=dict(showgrid=False, linecolor="#0c1c30", tickfont=dict(color="#0c1c30")),
        yaxis=dict(showgrid=True, gridcolor="#d1d5db", linecolor="#0c1c30", tickfont=dict(color="#0c1c30"))
    )
    st.plotly_chart(fig1, use_container_width=True)

with st.container():
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    df_bar = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    
    fig2 = px.bar(df_bar, x='stress_label', y='anxiety_level', color='stress_label',
                  color_discrete_map={"BAJO": "#2e7d32", "MODERADO": "#ffa15a", "ALTO": "#ef553b"})
    
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0c1c30"),
        xaxis_title="Nivel de Estrés",
        yaxis_title="Nivel de Ansiedad",
        xaxis=dict(tickfont=dict(color="#0c1c30")),
        yaxis=dict(tickfont=dict(color="#0c1c30")),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)
