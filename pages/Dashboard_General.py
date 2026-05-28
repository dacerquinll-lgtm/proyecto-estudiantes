import streamlit as st
import plotly.express as px

st.title("📊 Dashboard General de Datos Estudiantiles")
st.markdown("---")

# Verificamos si el dataset de estrés está cargado
if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    df_estres = st.session_state.datasets['estres']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución de Niveles de Estrés")
        fig_estres = px.histogram(
            df_estres, 
            x="stress_level", 
            nbins=3, 
            color="stress_level",
            labels={"stress_level": "Nivel de Estrés"},
            color_discrete_sequence=px.colors.qualitative.Safe,
            template="plotly_white"
        )
        st.plotly_chart(fig_estres, use_container_width=True)
        
    with col2:
        st.subheader("Relación: Sueño vs Rendimiento")
        fig_scatter = px.scatter(
            df_estres, 
            x="sleep_quality", 
            y="academic_performance", 
            color="stress_level",
            labels={"sleep_quality": "Calidad de Sueño", "academic_performance": "Rendimiento Académico"},
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.markdown("---")
    
    # Nueva sección analítica basada solo en el dataset de estrés
    st.subheader("Análisis de Factores de Riesgo")
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("Promedio de Ansiedad según Nivel de Estrés")
        df_promedio = df_estres.groupby('stress_level')['anxiety_level'].mean().reset_index()
        fig_bar = px.bar(df_promedio, x='stress_level', y='anxiety_level', color='stress_level')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col4:
        st.write("Impacto de la Presión de Pares en el Estrés")
        fig_box = px.box(df_estres, x="stress_level", y="peer_pressure", color="stress_level")
        st.plotly_chart(fig_box, use_container_width=True)

else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente las fuentes de datos.")
