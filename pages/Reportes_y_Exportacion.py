import streamlit as st

st.title("📄 Generador de Reportes y Exportación")
st.markdown("---")

# Verificamos si existe un diagnóstico previo en la sesión
if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos = diag['datos']  # Lista con los 10 valores
    resultado = diag['resultado']
    
    # Mapeo de resultados
    mapa_resultado = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
    nivel_txt = mapa_resultado.get(resultado, "Desconocido")
    
    st.success("✅ Diagnóstico previo detectado. Generando reporte dinámico.")
    
    # Entrada para personalización
    nombre = st.text_input("Nombre Completo del Estudiante:", "Estudiante")
    
    # Construcción del reporte con los datos dinámicos (índices de la lista 'datos')
    contenido_reporte = f"""--- REPORTE DE SALUD MENTAL Y ESTRÉS ---
Estudiante: {nombre}
Nivel de Estrés Detectado: {nivel_txt}

Métricas registradas:
- Ansiedad: {datos[0]}
- Autoestima: {datos[1]}
- Depresión: {datos[2]}
- Calidad de Sueño: {datos[3]}
- Rendimiento Académico: {datos[4]}
- Carga de Estudio: {datos[5]}
- Apoyo Social: {datos[6]}
- Presión de Pares: {datos[7]}
- Actividades Extras: {datos[8]}
- Bullying: {datos[9]}
----------------------------------------
"""
    
    st.markdown("### 📋 Vista Previa del Reporte")
    st.text_area("Contenido:", value=contenido_reporte, height=350)
    
    # Botón de descarga
    st.download_button(
        label="📥 Descargar Reporte Personalizado (TXT)",
        data=contenido_reporte,
        file_name=f"Reporte_{nombre.replace(' ', '_')}.txt",
        mime="text/plain"
    )

else:
    st.warning("⚠️ No se ha detectado un diagnóstico activo.")
    st.info("Por favor, ve a la página 'Detector de Estrés', ingresa tus datos y presiona 'Obtener Diagnóstico' para poder generar tu reporte.")
    
    # Opcional: Mostrar resumen estadístico si el dataset está cargado
    if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
        st.markdown("---")
        st.write("Estadísticas globales del sistema:")
        st.dataframe(st.session_state.datasets['estres'].describe())
