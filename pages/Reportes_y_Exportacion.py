import streamlit as st

st.title("📄 Generador de Reportes y Exportación de Datos")
st.markdown("---")

if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    df_estres = st.session_state.datasets['estres']
    df_burnout = st.session_state.datasets['burnout']
    
    st.markdown("### 📋 Resumen del Perfil Académico Global")
    
    total_alumnos_estres = len(df_estres)
    total_alumnos_burnout = len(df_burnout)
    
    promedio_sueno = float(df_estres['sleep_quality'].mean()) if 'sleep_quality' in df_estres.columns else 0.0
    promedio_ansiedad = float(df_estres['anxiety_level'].mean()) if 'anxiety_level' in df_estres.columns else 0.0
    
    val_col_b = df_burnout.select_dtypes(include=['float64', 'int64']).columns
    promedio_burnout = float(df_burnout[val_col_b[0]].mean()) if len(val_col_b) > 0 else 0.0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Muestra Total Analizada", value=f"{total_alumnos_estres} reg")
    with col2:
        st.metric(label="Promedio Calidad de Sueño", value=f"{promedio_sueno:.2f}")
    with col3:
        st.metric(label="Indicador Métrico Base", value=f"{promedio_burnout:.2f}")
        
    st.markdown("---")
    nombre_alumno = st.text_input("Nombre Completo del Estudiante:", "Estudiante Anónimo")
    codigo_alumno = st.text_input("Código o Identificador:", "000000")
    
    reporte_txt = f"Reporte de prueba para {nombre_alumno} ({codigo_alumno})"
    
    st.download_button(
        label="📥 Descargar Reporte Base TXT",
        data=reporte_txt,
        file_name=f"Reporte_{codigo_alumno}.txt",
        mime="text/plain"
    )
else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente las fuentes de datos.")
