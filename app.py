st.markdown("""
    <style>
    /* ... (mantén el resto de estilos igual) ... */
    
    /* Menú con azul ligeramente más claro */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) {
        background-color: #1a2a40 !important; 
        padding: 10px 20px !important;
        margin-top: 0px !important;
        margin-bottom: 30px !important;
        border-radius: 0 0 8px 8px !important;
        gap: 5px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) div[data-testid="stPageLink"] a {
        background-color: transparent !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 0.85rem !important;
        padding: 6px 10px !important;
        text-decoration: none !important;
    }
    
    /* Resaltado de página activa */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPageLink"]) > div[data-testid="column"]:nth-of-type(1) div[data-testid="stPageLink"] a {
        background-color: #2e7d32 !important;
        border-radius: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# CORRECCIÓN DE COLUMNAS: Ajusta los pesos para que quepan bien
cols_nav = st.columns([0.5, 1.2, 1.2, 1.4, 1.4]) 
with cols_nav[0]: st.page_link("app.py", label="Inicio")
with cols_nav[1]: st.page_link("pages/Dashboard_General.py", label="Dashboard General")
with cols_nav[2]: st.page_link("pages/Detector_de_Estres.py", label="Detector de Estrés")
with cols_nav[3]: st.page_link("pages/Reportes_y_Exportacion.py", label="Reportes y Exportación")
with cols_nav[4]: st.page_link("pages/Simulador_de_Escenarios.py", label="Simulador de Escenarios")
