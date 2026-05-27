import streamlit as st
import plotly.express as px

st.title("📈 Análisis Comparativo y Correlaciones de Variables")
st.markdown("---")

if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    df_estres = st.session_state.datasets['estres']
    df_burnout = st.session_state.datasets['burnout']
    
    st.markdown("### 🔍 Exploración Cruzada Interactiva")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Impacto del Sueño en el Desempeño Académico")
        fig_box_comp = px.box(
            df_estres,
            x="sleep_quality",
            y="academic_performance",
            color="stress_level",
            labels={
                "sleep_quality": "Calidad del Sueño (0-5)",
                "academic_performance": "Rendimiento Académico (0-5)",
                "stress_level": "Nivel de Estrés"
            },
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_box_comp, use_container_width=True)
        
    with col2:
        st.subheader("Distribución de Burnout Según Carga Horaria Semanal")
        fig_violin = px.violin(
            df_burnout,
            x="Workload",
            y="Burnout_Index",
            box=True,
            points="all",
            labels={
                "Workload": "Carga de Trabajo/Estudio (Horas)",
                "Burnout_Index": "Índice de Burnout"
            },
            color_discrete_sequence=["#00CC96"]
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        
    st.markdown("---")
    st.subheader("📊 Tabla de Datos Integrada para Análisis Rápido")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        mostrar_tabla = st.checkbox("Mostrar registros del Dataset de Estrés", value=False)
    with col_sel2:
        mostrar_tabla_b = st.checkbox("Mostrar registros del Dataset de Burnout", value=False)
        
    if mostrar_tabla:
        st.dataframe(df_estres.head(100), use_container_width=True)
        
    if mostrar_tabla_b:
        st.dataframe(df_burnout.head(100), use_container_width=True)
else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente las fuentes de datos del sistema.")