import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS DE PRECISIÓN AMATISTA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #1a0a2e;
    }

    .stApp {
        background-color: #1a0a2e;
    }

    /* Título Neón (Intacto) */
    .main-title {
        text-align: center;
        color: #fff !important;
        font-size: 3.2rem !important;
        font-weight: 600;
        margin-bottom: 50px !important;
        padding-top: 20px;
        text-shadow: 0 0 10px #ff4081, 0 0 20px #ff4081;
    }

    /* --- BOTONES DE GÉNERO (MORADO CLARO) --- */
    
    /* El contenedor principal del botón desplegable */
    div[data-testid="stExpander"] details summary {
        background-color: #3d1c52 !important; /* Morado más claro que el fondo */
        border-radius: 12px !important;
        border: 1px solid #7b1fa2 !important;
        padding: 15px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }

    /* Forzamos que el texto del título sea BLANCO */
    div[data-testid="stExpander"] details summary p {
        color: #ffffff !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }

    /* Flecha en blanco */
    div[data-testid="stExpander"] details summary svg {
        fill: #ffffff !important;
    }

    /* FIX: Evitar que el fondo se vuelva blanco al hacer focus o clic */
    div[data-testid="stExpander"] details summary:hover, 
    div[data-testid="stExpander"] details summary:focus,
    div[data-testid="stExpander"] details summary:active {
        background-color: #4a2366 !important; /* Un morado ligeramente más vibrante al tocarlo */
        color: #ffffff !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Estilo del contenido interior */
    .streamlit-expanderContent {
        background-color: #26123d !important;
        border: 1px solid #3d1c52 !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
    }

    /* --- TEXTO DENTRO DE LOS INPUTS --- */
    input {
        background-color: #1a0a2e !important;
        color: #ffffff !important; /* Texto del usuario en blanco */
        border: 1px solid #7b1fa2 !important;
        border-radius: 10px !important;
        text-align: center;
    }

    /* Botón de Buscar e Interfaz */
    .stButton>button {
        background: linear-gradient(45deg, #7b1fa2, #ff4081);
        color: white !important;
        border-radius: 25px;
        width: 100%;
        border: none;
    }
    
    .centered-text {
        text-align: center;
        color: #fce4ec !important;
    }

    .stProgress > div > div > div > div {
        background-color: #ff4081;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA ---
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
st.markdown('<h1 class="main-title">¿Cuándo fue la última vez que leíste?</h1>', unsafe_allow_html=True)
st.markdown('<p class="centered-text">Escribe la respuesta correcta para activar cada escudo literario.</p>', unsafe_allow_html=True)

for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
    emoji = "✅" if st.session_state.progreso[genero] else "📖"
    with st.expander(f"{genero.upper()} {emoji}"):
        # Texto blanco para el label
        st.markdown(f'<p style="color: #fce4ec;">¿Cuál es el secreto de {genero}?</p>', unsafe_allow_html=True)
        user_input = st.text_input("", key=f"input_{genero}", label_visibility="collapsed").lower().strip()
        
        if user_input == respuesta_real:
            st.session_state.progreso[genero] = True
            st.success("Escudo activado.")
        elif user_input != "":
            st.error("Sigue intentando.")

# --- SECCIÓN FINAL ---
if all(st.session_state.progreso.values()):
    st.divider()
    st.balloons()
    st.markdown("""
        <div style="background-color: #2e1a47; border: 3px dashed #ff4081; padding: 30px; border-radius: 20px; text-align: center;">
            <h2 style="color: white !important;">¡LOGRADO! ⊹ ࣪ ˖</h2>
            <p style="color: #fce4ec;">Usa el código en tu próxima compra:</p>
            <h1 style="color: #ff80ab !important; font-size: 35px;">LECTURA15OFF</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    completados = sum(st.session_state.progreso.values())
    st.progress(completados / 5)
    st.markdown(f'<p class="centered-text">Has encontrado {completados} de 5 secretos.</p>', unsafe_allow_html=True)
