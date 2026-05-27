import streamlit as st

st.title("📄 Generador de Reportes y Exportación de Datos")
st.markdown("---")

if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
    df_estres = st.session_state.datasets['estres']
    df_burnout = st.session_state.datasets['burnout']
    
    st.markdown("### 📋 Resumen del Perfil Académico Global")
    
    total_alumnos_estres = len(df_estres)
    total_alumnos_burnout = len(df_burnout)
    
    promedio_sueno = float(df_estres['sleep_quality'].mean())
    promedio_ansiedad = float(df_estres['anxiety_level'].mean())
    promedio_burnout = float(df_burnout['Burnout_Index'].mean())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Promedio Calidad de Sueño (0-5)", value=f"{promedio_sueno:.2f}")
    with col2:
        st.metric(label="Promedio Nivel de Ansiedad (0-21)", value=f"{promedio_ansiedad:.2f}")
    with col3:
        st.metric(label="Índice Promedio de Burnout", value=f"{promedio_burnout:.2f}")
        
    st.markdown("---")
    st.markdown("### 💾 Exportar Reporte de Diagnóstico Estudiantil")
    
    st.markdown("Complete los datos del alumno para estructurar el archivo de descarga:")
    
    nombre_alumno = st.text_input("Nombre Completo del Estudiante:", "Estudiante Anónimo")
    codigo_alumno = st.text_input("Código o Identificador:", "000000")
    observaciones = st.text_area("Notas u Observaciones Adicionales:", "Sin observaciones.")
    
    reporte_txt = f"""==================================================
REPORTE DE BIENESTAR Y SALUD MENTAL ESTUDIANTIL
==================================================
Identificación del Alumno:
- Nombre: {nombre_alumno}
- Código: {codigo_alumno}

Métricas de Referencia del Sistema:
- Muestra total analizada (Estrés): {total_alumnos_estres} registros
- Muestra total analizada (Burnout): {total_alumnos_burnout} registros
- Calidad de sueño promedio del entorno: {promedio_sueno:.2f}/5
- Nivel de ansiedad promedio del entorno: {promedio_ansiedad:.2f}/21
- Índice de burnout promedio del entorno: {promedio_burnout:.2f}

Observaciones del Evaluador:
{observaciones}
==================================================
Reporte generado automáticamente por la Plataforma Web.
"""
    
    st.markdown(" ")
    st.download_button(
        label="📥 Descargar Reporte en Formato TXT",
        data=reporte_txt,
        file_name=f"Reporte_Bienestar_{codigo_alumno}.txt",
        mime="text/plain"
    )
else:
    st.error("Por favor, regresa a la página de Inicio (app.py) para inicializar correctamente las fuentes de datos del sistema.")