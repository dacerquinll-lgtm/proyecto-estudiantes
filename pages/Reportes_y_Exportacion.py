import streamlit as st

st.title("📄 Generador de Reportes y Exportación")
st.markdown("---")

# Verificamos si existe un diagnóstico previo en la sesión
if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos = diag['datos']  # Lista con las 8 respuestas
    estres = diag['estres'] # Resultado del modelo (0, 1, 2)
    rendimiento = diag['rendimiento'] # Resultado de la lógica (0, 1, 2)
    
    # Mapeos
    mapa_estres = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
    mapa_rend = {0: "MALO", 1: "IRREGULAR", 2: "ALTO"}
    
    st.success("✅ Diagnóstico previo detectado. Generando reporte.")
    
    nombre = st.text_input("Nombre Completo del Estudiante:", "Estudiante")
    
    # Construcción del reporte ajustado a las 8 métricas reales
    contenido_reporte = f"""--- REPORTE INTEGRAL ACADÉMICO ---
Estudiante: {nombre}
Nivel de Estrés Detectado: {mapa_estres.get(estres)}
Proyección de Rendimiento: {mapa_rend.get(rendimiento)}

Métricas registradas:
- Ansiedad: {datos[0]}
- Autoestima: {datos[1]}
- Depresión: {datos[2]}
- Calidad de Sueño: {datos[3]}
- Carga de Estudio: {datos[4]}
- Actividades Extras: {datos[5]}
- Apoyo Social: {datos[6]}
- Rendimiento Previo/Interés: {datos[7]}
----------------------------------------
"""
    
    st.markdown("### 📋 Vista Previa del Reporte")
    st.text_area("Contenido:", value=contenido_reporte, height=300)
    
    st.download_button(
        label="📥 Descargar Reporte (TXT)",
        data=contenido_reporte,
        file_name=f"Reporte_{nombre.replace(' ', '_')}.txt",
        mime="text/plain"
    )

else:
    st.warning("⚠️ No se ha detectado un diagnóstico activo.")
    st.info("Por favor, completa el diagnóstico en el detector para generar el reporte.")
