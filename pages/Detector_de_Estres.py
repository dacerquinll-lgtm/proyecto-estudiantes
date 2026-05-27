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
        fig_estres = px.histogram(
            df_estres, 
            x="stress_level", 
            nbins=3, 
            color="stress_level",
            labels={"stress_level": "Nivel de Estrés"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_estres, use_container_width=True)
        
    with col2:
        st.subheader("Relación: Horas de Sueño vs Carga Académica")
        fig_scatter = px.scatter(
            df_estres, 
            x="sleep_quality", 
            y="academic_performance", 
            color="stress_level",
            labels={"sleep_quality": "Calidad de Sueño", "academic_performance": "Rendimiento Académico"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Análisis de Salud Mental y Burnout (Muestra Recortada)")
    
    if df_burnout is not None:
        col3, col4 = st.columns(2)
        
        with col3:
            fig_box = px.box(
                df_burnout, 
                x="Gender", 
                y="Workload", 
                color="Damaging_Mental_Health_History",
                labels={"Workload": "Carga de Trabajo/Estudio", "Gender": "Género"}
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
        with col4:
            fig_pie = px.pie(
                df_burnout, 
                names="Anxiety_Mental_Health_History", 
                hole=0.4,
                title="Historial de Ansiedad Registrado"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente las fuentes de datos del sistema.")