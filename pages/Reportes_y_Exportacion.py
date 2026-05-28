import streamlit as st
import pandas as pd

st.title("📄 Generador de Reportes y Exportación")
st.markdown("---")

# 1. Verificamos si existe un diagnóstico reciente del usuario
if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos = diag['datos']
    resultado = diag['resultado']
    
    st.success("✅ Diagnóstico detectado. Procediendo a generar reporte personalizado.")
    
    # Mapeo de resultados
    mapa_resultado = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
    nivel_txt = mapa_resultado.get(resultado, "Desconocido")
    
    # 2. Captura de datos del usuario para el reporte
    nombre = st.text_input("Nombre Completo:", "Estudiante")
    
    # 3. Construcción del contenido del reporte
    contenido_reporte = f"""
    --- REPORTE DE SALUD MENTAL Y ESTRÉS ---
    Estudiante: {nombre}
    Nivel de Estrés Detectado: {nivel_txt}
    
    Métricas ingresadas:
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
    
    st.text_area("Vista previa del reporte:", contenido_reporte, height=300)
    
    # 4. Botón de descarga
    st.download_button(
        label="📥 Descargar Reporte Personalizado (TXT)",
        data=contenido_reporte,
        file_name=f"Reporte_Estres_{nombre}.txt",
        mime="text/plain"
    )

else:
    st.warning("⚠️ No se ha realizado un diagnóstico previo.")
    st.info("Por favor, dirígete a la página **Detector de Estrés** para completar tu evaluación antes de generar un reporte.")
    
    # Opcional: Mostrar indicadores generales si quieres mantener algo de info global
    if 'datasets' in st.session_state and st.session_state.datasets.get('estres') is not None:
        st.markdown("---")
        st.write("Estadísticas globales disponibles (sin diagnóstico personal):")
        st.write(st.session_state.datasets['estres'].describe())
