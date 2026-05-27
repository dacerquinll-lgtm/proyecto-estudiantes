import streamlit as st
import plotly.express as px

st.title("📊 Dashboard General")
df = st.session_state.datasets.get('estres')

if df is not None:
    # Usamos nombres normalizados
    fig1 = px.histogram(df, x="stress_level", color="stress_level")
    st.plotly_chart(fig1, use_container_width=True)
    
    # render_mode="svg" evita el error de WebGL
    fig2 = px.scatter(df, x="sleep_quality", y="study_hours", color="stress_level", render_mode="svg")
    st.plotly_chart(fig2, use_container_width=True)
