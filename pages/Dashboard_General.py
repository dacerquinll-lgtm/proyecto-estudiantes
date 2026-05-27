import streamlit as st
import plotly.express as px

st.title("📊 Dashboard General de Datos Estudiantiles")
st.markdown("---")

# Verificamos que los datos existan en la sesión global
if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    df_estres = st.session_state.datasets['estres']
    df_burnout = st.session_state.datasets['burnout']
    
    col1, col2 = st.columns(2)
    
    # Gráfico 1: Distribución de Estrés
    with col1:
        st.subheader("Distribución de Niveles de Estrés")
        # Usamos 'stress_level' porque app.py ya lo normalizó
        fig1 = px.histogram(
            df_estres, 
            x="stress_level", 
            color="stress_level",
            labels={"stress_level": "Nivel de Estrés"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    # Gráfico 2: Calidad de Sueño vs Horas de Estudio
    with col2:
        st.subheader("Relación: Calidad de Sueño vs Horas de Estudio")
        # Usamos los nombres normalizados: sleep_quality y study_hours
        fig2 = px.scatter(
            df_estres, 
            x="sleep_quality", 
            y="study_hours", 
            color="stress_level",
            labels={"sleep_quality": "Calidad de Sueño", "study_hours": "Horas de Estudio"},
            render_mode="svg" # Evita errores de WebGL
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Análisis de Burnout Estudiantil")
    
    # Verificamos si existe burnout_score o usamos la segunda columna numérica
    if 'burnout_score' in df_burnout.columns:
        col_b = 'burnout_score'
    else:
        # Selecciona la primera columna numérica que encuentre para evitar KeyError
        num_cols = df_burnout.select_dtypes(include=['number']).columns
        col_b = num_cols[1] if len(num_cols) > 1 else num_cols[0]
        
    fig3 = px.box(
        df_burnout, 
        y=col_b,
        labels={col_b: "Índice de Burnout"},
        color_discrete_sequence=["#FF6692"]
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.error("Los datos no están cargados. Por favor, ve primero a la página de Inicio (app.py) para inicializar el sistema.")
