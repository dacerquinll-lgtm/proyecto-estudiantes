import streamlit as st
import plotly.express as px

st.title("📈 Análisis Comparativo y Correlaciones de Variables")
st.markdown("---")

# Verificamos si el dataset de estrés está en la sesión
if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    df_estres = st.session_state.datasets['estres']
    
    st.markdown("### 🔍 Exploración Interactiva del Estrés Académico")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Impacto del Sueño en el Rendimiento")
        # Aseguramos nombres de columnas estándar (ajusta si tus columnas tienen otros nombres)
        fig_box = px.box(
            df_estres,
            x="sleep_quality",
            y="academic_performance",
            color="stress_level",
            labels={
                "sleep_quality": "Calidad del Sueño",
                "academic_performance": "Rendimiento Académico",
                "stress_level": "Nivel de Estrés"
            },
            template="plotly_white"
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col2:
        st.subheader("Distribución de Ansiedad por Estrés")
        # Usamos variables relevantes del dataset de estrés
        fig_violin = px.violin(
            df_estres,
            x="stress_level",
            y="anxiety_level",
            box=True,
            points="all",
            color="stress_level",
            labels={
                "stress_level": "Nivel de Estrés",
                "anxiety_level": "Nivel de Ansiedad"
            },
            template="plotly_white"
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        
    st.markdown("---")
    st.info("💡 Este análisis permite identificar visualmente qué factores (como la calidad del sueño o la ansiedad) tienen una correlación más fuerte con el nivel de estrés registrado.")

else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente el dataset.")
