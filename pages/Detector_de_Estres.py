import streamlit as st
import joblib
import numpy as np
import os

# Configuración de página centrada con diseño institucional
st.set_page_config(page_title="Detector de Estrés", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS institucionales y estructura limpia de tarjetas
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa !important; }
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
    .header-institucional {
        background-color: #0c1c30;
        padding: 20px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
        border-radius: 8px 8px 0 0;
    }
    .header-institucional h2 { color: white !important; margin: 0; font-size: 1.2rem !important; font-weight: 600 !important; }
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        background-color: #1a2a40 !important;
        padding: 10px 20px !important;
        margin-bottom: 30px !important;
        border-radius: 0 0 8px 8px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) a {
        color: #ffffff !important; font-weight: bold !important; text-decoration: none !important;
    }
    
    /* Contenedor tipo Tarjeta Blanca (Prototipo) */
    .tarjeta-evaluacion {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }
    
    /* Corrección de color de textos de sliders para que se vean en fondo claro */
    .stSlider label, .stSlider span, .stSlider div {
        color: #0c1c30 !important;
    }
    
    .stProgress > div > div > div > div {
        background-color: #2e7d32 !important;
    }
    
    h1, h2, h3, h4 { color: #0c1c30 !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color: #0c1c30 !important; }
    div[data-testid="stMetric"] { padding: 15px !important; border-radius: 8px !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08) !important; }
    
    /* Personalización de Métricas de Resultados */
    div[data-testid="column"]:has(div[data-testid="stMetric"]):nth-of-type(1) div[data-testid="stMetric"] { background-color: #ffebee !important; border: 1px solid #ffcdd2 !important; }
    div[data-testid="column"]:has(div[data-testid="stMetric"]):nth-of-type(2) div[data-testid="stMetric"] { background-color: #e3f2fd !important; border: 1px solid #90caf9 !important; }
    
    div.stButton > button {
        background-color: #2e7d32 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        padding: 10px 24px !important;
    }
    div.stButton > button:hover {
        background-color: #1b5e20 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Institucional
st.markdown("""
    <div class="header-institucional">
        <div><span style="font-weight: 900; font-size: 1.6rem; color: #e53935;">UCV</span></div>
        <div><h2>Sistema Inteligente para la Reducción de Estrés en Universitarios</h2></div>
    </div>
""", unsafe_allow_html=True)

# Menú de Navegación Sincronizado
cols_nav = st.columns([0.8, 1.2, 1.2, 1.4, 1.4])
with cols_nav[0]: st.page_link("app.py", label="Inicio")
with cols_nav[1]: st.page_link("pages/Dashboard_General.py", label="Dashboard General")
with cols_nav[2]: st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés")
with cols_nav[3]: st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación")
with cols_nav[4]: st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios")

st.title("🧠 Detector Integral Académico")

# --- INICIALIZACIÓN ROBUSTA ---
if 'iniciado' not in st.session_state:
    st.session_state.update({'respuestas': [], 'iniciado': False})

# --- PANTALLA DE BIENVENIDA ---
if not st.session_state.iniciado:
    st.markdown("""
        <div class="tarjeta-evaluacion">
            <h3 style="margin-top:0;">Evaluación de hábitos académicos</h3>
            <p style="color: #4a5568; line-height: 1.6;">
                Este sistema implementa modelos de <b>Aprendizaje Automático (Machine Learning)</b> para analizar tus hábitos académicos y niveles de estrés. 
                Al completar este cuestionario de 8 preguntas, el algoritmo procesará tus variables para brindarte un diagnóstico proyectado y recomendaciones personalizadas.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Comenzar Test"):
        st.session_state.iniciado = True
        st.rerun()

# --- FORMULARIO COMPLETO DE PREGUNTAS (Estilo Prototipo Fig. A2) ---
elif len(st.session_state.respuestas) == 0:
    st.markdown("### Evaluación de Hábitos Académicos")
    st.markdown('<p style="color: #666;">Responde las siguientes preguntas para que el sistema pueda analizar tu nivel de estrés.</p>', unsafe_allow_html=True)
    
    # Formulario para agrupar todas las preguntas
    with st.form("formulario_evaluacion"):
        
        # Fila 1
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            ansiedad = st.slider("1. ¿Cuál es tu nivel de ansiedad actual? (1=Extrema, 10=Ninguna)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            confianza = st.slider("2. ¿Qué nivel de confianza tienes en ti mismo/a? (1=Muy baja, 10=Muy alta)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Fila 2
        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            animo = st.slider("3. ¿Cómo calificarías tu estado de ánimo general? (1=Muy decaído, 10=Muy optimista)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_d:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            sueno = st.slider("4. ¿Cómo es la calidad de tu sueño? (1=Muy mala, 10=Excelente)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Fila 3
        col_e, col_f = st.columns(2)
        with col_e:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            carga = st.slider("5. ¿Qué capacidad tienes para manejar tu carga de estudio? (1=Desbordado/a, 10=Control total)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_f:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            recreativo = st.slider("6. ¿Qué tanto tiempo dedicas a actividades recreativas? (1=Nada, 10=Lo suficiente)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Fila 4
        col_g, col_h = st.columns(2)
        with col_g:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            apoyo = st.slider("7. ¿Cuánto apoyo social sientes que recibes? (1=Nada, 10=Muchísimo)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_h:
            st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
            interes = st.slider("8. ¿Cómo es tu interés académico? (1=Muy bajo, 10=Excelente)", 1, 10, 5)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Botón de envío del formulario
        enviar = st.form_submit_button("📊 Analizar nivel de estrés")
        if enviar:
            st.session_state.respuestas = [ansiedad, confianza, animo, sueno, carga, recreativo, apoyo, interes]
            st.rerun()

# --- PANTALLA DE RESULTADOS PROFESIONAL (Estilo Prototipo Fig. A3 y A4) ---
else:
    ruta_modelo = "modelos/modelo_stress_rf.pkl"
    if not os.path.exists(ruta_modelo):
        st.error(f"Error: No se encuentra el archivo en {ruta_modelo}")
        st.stop()
        
    modelo = joblib.load(ruta_modelo)
    estres = modelo.predict(np.array([st.session_state.respuestas]))[0] # 0: BAJO, 1: MODERADO, 2: ALTO
    rendimiento = 2 - estres 
    
    # GUARDADO PARA EL REPORTE
    st.session_state['ultimo_diagnostico'] = {
        'datos': st.session_state.respuestas,
        'estres': estres,
        'rendimiento': rendimiento
    }
    
    st.markdown("""
        <div class="tarjeta-evaluacion">
            <h3 style="margin-top:0; color: #0c1c30;">📋 Resultado de tu evaluación</h3>
            <p style="color: #666; font-size: 0.95rem;">El sistema ha analizado tus respuestas utilizando modelos de Machine Learning.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas visuales
    col1, col2 = st.columns(2)
    col1.metric("Nivel de Estrés Predicho", ["BAJO", "MODERADO", "ALTO"][estres])
    col2.metric("Rendimiento Académico Proyectado", ["MALO", "IRREGULAR", "ALTO"][rendimiento])
    
    st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
    
    # Recomendación general según nivel (Información completa)
    recs = [
        "Mantén hábitos saludables y organiza tus tareas pendientes.",
        "Prioriza el descanso y aplica técnicas de gestión del tiempo.",
        "Es momento de tomar acción inmediata para proteger tu bienestar emocional."
    ]
    
    st.markdown('<div class="tarjeta-evaluacion">', unsafe_allow_html=True)
    st.markdown(f"#### Recomendaciones sugeridas")
    st.write(f"💡 **Sugerencia Estratégica:** {recs[estres]}")
    
    # Análisis académico extra
    analisis = ["Necesitas tutorías extra.", "Organiza mejor tus tiempos.", "¡Excelente ritmo, continúa así!"]
    st.info(f"📊 **Análisis Académico:** {analisis[rendimiento]}")
    
    # Bloque EXTRA si el estrés es ALTO
    if estres == 2:
        st.warning("⚠️ **Nota de Atención Profesional:**")
        st.markdown("""
        Due to high stress indicators, we recommend:
        - **Buscar apoyo profesional:** Considera agendar una cita con el psicólogo del área de Bienestar Universitario.
        - **Desconexión:** Reduce actividades académicas no esenciales por 48 horas.
        - **Comunicación:** Habla con un tutor o docente de confianza sobre tu situación actual.
        *Tu salud es prioridad sobre cualquier calificación.*
        """)
    else:
        st.success("¡Excelente! Continúa monitoreando tu bienestar para mantener este equilibrio.")
    
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 Reiniciar Evaluación"):
        st.session_state.respuestas = []
        st.session_state.iniciado = False
        if 'ultimo_diagnostico' in st.session_state:
            del st.session_state['ultimo_diagnostico']
        st.rerun()
