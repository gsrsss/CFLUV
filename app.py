import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #1a0a2e;
    }

    .stApp {
        background-color: #1a0a2e;
    }

    /* Centrado de títulos y textos */
    .main-title {
        text-align: center;
        color: #fce4ec !important;
        font-size: 3rem !important; /* Más grande */
        font-weight: 600;
        margin-bottom: 40px !important; /* Espacio extra abajo */
        padding-top: 20px;
    }

    .centered-text {
        text-align: center;
        color: #fce4ec !important;
        margin-bottom: 25px !important;
    }

    h3 {
        text-align: center;
        color: #fce4ec !important;
    }

    /* Estilo para los Expanders */
    .streamlit-expanderHeader {
        background-color: #3d1c52 !important;
        border-radius: 10px !important;
        color: #ff80ab !important;
        text-align: center;
    }

    /* Contenedor del Cupón */
    .coupon-container {
        background-color: #2e1a47;
        border: 2px dashed #ff4081;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0px 0px 15px rgba(255, 64, 129, 0.3);
    }

    .coupon-code {
        font-size: 24px;
        font-weight: bold;
        color: #ba68c8;
        letter-spacing: 2px;
    }

    /* Botones */
    .stButton>button {
        background: linear-gradient(45deg, #7b1fa2, #ff4081);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 25px;
        transition: all 0.3s ease;
        font-weight: 600;
        display: block;
        margin: 0 auto; /* Centrar botón de buscar */
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 12px rgba(255, 64, 129, 0.6);
    }
    
    /* Inputs */
    input {
        background-color: #2e1a47 !important;
        color: white !important;
        border: 1px solid #7b1fa2 !important;
        border-radius: 10px !important;
        text-align: center; /* Texto centrado en el input */
    }

    /* Ajuste de progreso centrado */
    .stProgress {
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
RESPUESTAS_CORRECTAS = {
    "Romance": "corazon",
    "Fantasía": "dragon",
    "Ficción": "espejo",
    "No-Ficción": "verdad",
    "Misterio": "llave"
}

if 'progreso' not in st.session_state:
    st.session_state.progreso = {genero: False for genero in RESPUESTAS_CORRECTAS}

# --- INTERFAZ ---
# Título principal centrado y grande
st.markdown('<h1 class="main-title">¿Cuándo fue la última vez que leíste?</h1>', unsafe_allow_html=True)
st.markdown('<p class="centered-text">Introduce las respuestas que encontraste en los libros para desbloquear un secreto...</p>', unsafe_allow_html=True)

# Espacio adicional antes de los géneros
st.write("")

for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
    with st.expander(f"Género: {genero} {'✅' if st.session_state.progreso[genero] else '🔍'}"):
        user_input = st.text_input(f"Respuesta para {genero}:", key=f"input_{genero}").lower().strip()
        
        if user_input == respuesta_real:
            st.session_state.progreso[genero] = True
            st.success(f"¡Correcto! Has encontrado el escudo de {genero}.")
        elif user_input != "":
            st.error("Esa no es la respuesta, ¡sigue buscando en el libro!")

# --- SECCIÓN DE RECOMPENSA ---
todos_completados = all(st.session_state.progreso.values())

if todos_completados:
    st.divider()
    st.balloons()
    st.markdown("""
        <div class="coupon-container">
            <h3>¡Felicitaciones! ⊹ ࣪ ˖</h3>
            <p>Lograste encontrar todos los escudos y responder el acertijo.</p>
            <p>Desbloqueaste el secreto:</p>
            <div class="coupon-code">LECTURA15OFF</div>
            <p><small>Válido para los libros incluidos en la promoción especial.</small></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="margin-bottom: 20px;">Cuéntale a la biblioteca mágica lo que buscas, y te dirá cuál será tu próxima lectura.</h3>', unsafe_allow_html=True)
    
    query = st.text_input("Buscador de libros", placeholder="Ej. quiero un libro de misterio y romance...", label_visibility="collapsed")
    buscar = st.button("Buscar")

    if buscar and query:
        with st.spinner("Consultando con la biblioteca mágica..."):
            st.info(f"Basado en tu búsqueda '{query}', te recomendamos leer **'La Sombra del Viento'** de Carlos Ruiz Zafón.")
else:
    # Barra de progreso visual centraday texto
    completados = sum(st.session_state.progreso.values())
    st.progress(completados / len(RESPUESTAS_CORRECTAS))
    st.markdown(f'<p class="centered-text">Has desbloqueado {completados} de {len(RESPUESTAS_CORRECTAS)} géneros.</p>', unsafe_allow_html=True)
