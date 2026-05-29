import streamlit as st
import plotly.express as px
import pandas as pd
import os

# 1. Configuración de página
st.set_page_config(page_title="Analytics Central", layout="wide")

# 2. CSS profesional
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; }
    h1, h2, h3 { color: #ffffff !important; }
    .stPlotlyChart { background-color: #1e1e26; border-radius: 15px; }
    .guia-box { 
        background-color: #262730; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #ffffff; margin-bottom: 20px; 
    }
    </style>
""", unsafe_allow_html=True)

# 3. Carga automática de datos
if 'datasets' not in st.session_state:
    ruta = os.path.join("datasets", "StressLevelDataset_limpio.csv")
    if os.path.exists(ruta):
        st.session_state['datasets'] = {'estres': pd.read_csv(ruta)}
    else:
        st.error("❌ Archivo no encontrado en /datasets/")
        st.stop()

df = st.session_state.datasets['estres']

# Mapeo de niveles y colores (Consistente para todo el dashboard)
mapa_label = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
colores_niveles = {
    "BAJO": "#00cc96", 
    "MODERADO": "#ffa15a", 
    "ALTO": "#ef553b"
}
df['stress_label'] = df['stress_level'].map(mapa_label)

# 4. Interfaz
st.title("📊 Centro de Analítica Estudiantil")

# Leyenda explicativa visible
st.markdown("""
<div class="guia-box">
    <strong>Guía de Clasificación de Estrés:</strong> 
    <span style="color: #00cc96;">● Nivel 0: BAJO</span> | 
    <span style="color: #ffa15a;">● Nivel 1: MODERADO</span> | 
    <span style="color: #ef553b;">● Nivel 2: ALTO</span>
</div>
""", unsafe_allow_html=True)

# KPIs
promedio_estres_num = int(round(df['stress_level'].mean()))
col1, col2, col3 = st.columns(3)
col1.metric("Total Estudiantes", len(df))
col2.metric("Nivel de Estrés Promedio", mapa_label.get(promedio_estres_num, "N/A"))
col3.metric("Ansiedad Promedio", round(df['anxiety_level'].mean(), 2))

st.markdown("---")

# Gráficos en TABS
tab1, tab2 = st.tabs(["📉 Análisis de Rendimiento", "⚠️ Factores de Riesgo"])

with tab1:
    st.subheader("Distribución del Rendimiento vs Estrés")
    # Gráfico de Violín: muestra densidad y distribución de los datos
    fig = px.violin(df, x="stress_label", y="academic_performance", 
                    color="stress_label", box=True, points="all",
                    template="plotly_dark", color_discrete_map=colores_niveles,
                    labels={"stress_label": "Nivel de Estrés", 
                            "academic_performance": "Rendimiento Académico"})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Promedio de Ansiedad por Nivel de Estrés")
    
    # Agrupamos y ordenamos para que el gráfico sea lógico
    df_box = df.groupby(['stress_label'])['anxiety_level'].mean().reset_index()
    orden = ["BAJO", "MODERADO", "ALTO"]
    df_box['stress_label'] = pd.Categorical(df_box['stress_label'], categories=orden, ordered=True)
    df_box = df_box.sort_values('stress_label')
    
    fig2 = px.bar(df_box, x='stress_label', y='anxiety_level', 
                  color='stress_label', template="plotly_dark",
                  color_discrete_map=colores_niveles,
                  labels={"stress_label": "Nivel de Estrés",
                          "anxiety_level": "Nivel Promedio de Ansiedad"})
    st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **Interpretación:** El gráfico de violín revela cómo se concentra el rendimiento académico según el estrés, validando el impacto negativo del estrés alto.")
