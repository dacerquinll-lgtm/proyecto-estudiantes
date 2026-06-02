import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.title("📄 Generador de Reportes y Exportación")
st.markdown("---")

if 'ultimo_diagnostico' in st.session_state:
    diag = st.session_state['ultimo_diagnostico']
    datos = diag['datos']
    estres = diag['estres']
    rendimiento = diag['rendimiento']
    
    mapa_estres = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}
    mapa_rend = {0: "MALO", 1: "IRREGULAR", 2: "ALTO"}
    
    st.success("✅ Diagnóstico detectado. Generando PDF.")
    nombre = st.text_input("Nombre Completo del Estudiante:", "Estudiante")

    # Función para generar el PDF en memoria
    def generar_pdf(nombre, estres_txt, rend_txt, datos):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "REPORTE INTEGRAL ACADÉMICO")
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Estudiante: {nombre}")
        c.drawString(50, 700, f"Nivel de Estrés: {estres_txt}")
        c.drawString(50, 680, f"Proyección de Rendimiento: {rend_txt}")
        
        c.drawString(50, 650, "Métricas registradas:")
        y = 630
        labels = ["Ansiedad", "Autoestima", "Depresión", "Calidad de Sueño", 
                  "Carga de Estudio", "Actividades Extras", "Apoyo Social", "Interés Académico"]
        for i, label in enumerate(labels):
            c.drawString(70, y, f"- {label}: {datos[i]}")
            y -= 20
        c.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = generar_pdf(nombre, mapa_estres.get(estres), mapa_rend.get(rendimiento), datos)
    
    st.download_button(
        label="📥 Descargar Reporte (PDF)",
        data=pdf_buffer,
        file_name=f"Reporte_{nombre.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

else:
    st.warning("⚠️ No se ha detectado un diagnóstico activo.")
