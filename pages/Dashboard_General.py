import streamlit as st
import plotly.express as px

st.title("📊 Dashboard General de Datos Estudiantiles")
st.markdown("---")

if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    df_estres = st.session_state.datasets['estres']
    df_burnout = st.session_state.datasets['burnout']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución de Niveles de Estrés")
        fig1 = px.histogram(
            df_estres, 
            x="stress_level", 
            color="stress_level",
            labels={"stress_level": "Nivel de Estrés"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.subheader("Relación: Calidad de Sueño vs Horas de Estudio")
        fig2 = px.scatter(
            df_estres, 
            x="sleep_quality", 
            y="study_hours", 
            color="stress_level",
            labels={"sleep_quality": "Calidad de Sueño", "study_hours": "Horas de Estudio"},
            render_mode="svg"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Análisis de Burnout Estudiantil")
    
    if 'burnout_score' in df_burnout.columns:
        col_b = 'burnout_score'
    else:
        col_b = df_burnout.columns[1]
        
    fig3 = px.box(
        df_burnout, 
        y=col_b,
        labels={col_b: "Índice de Burnout"},
        color_discrete_sequence=["#FF6692"]
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente las fuentes de datos.")
