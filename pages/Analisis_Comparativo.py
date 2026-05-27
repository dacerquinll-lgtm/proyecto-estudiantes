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
        st.subheader("Impacto del Sueño en el Rendimiento")
        y_col = "academic_performance" if "academic_performance" in df_estres.columns else df_estres.columns[0]
        fig_box_comp = px.box(
            df_estres,
            x="sleep_quality",
            y=y_col,
            color="stress_level",
            labels={
                "sleep_quality": "Calidad del Sueño",
                y_col: "Rendimiento Académico",
                "stress_level": "Nivel de Estrés"
            }
        )
        st.plotly_chart(fig_box_comp, use_container_width=True)
        
    with col2:
        st.subheader("Distribución Genérica de Carga de Trabajo")
        col_x = df_burnout.columns[0]
        col_y = df_burnout.columns[1]
        
        fig_violin = px.violin(
            df_burnout,
            x=col_x,
            y=col_y,
            box=True,
            points="all",
            color_discrete_sequence=["#00CC96"]
        )
        st.plotly_chart(fig_violin, use_container_width=True)
else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente las fuentes de datos.")
