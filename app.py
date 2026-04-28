import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS DE FUERZA BRUTA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

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
        text-shadow: 0 0 10px #ff4081, 0 0 20px #ff4081;
    }

    /* --- NUEVO ESTILO DE BOTONES DE GÉNERO --- */
    /* Forzamos el contenedor del expander */
    .st-emotion-cache-p5msec {
        background-color: #f06292 !important; /* Rosa sólido */
        border-radius: 15px !important;
        border: 2px solid #ff80ab !important;
        margin-bottom: 15px !important;
    }

    /* EL TRUCO: Forzar CUALQUIER texto dentro del encabezado a ser blanco */
    div[data-testid="stExpander"] details summary p {
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Color de la flecha */
    div[data-testid="stExpander"] details summary svg {
        fill: #FFFFFF !important;
    }

    /* Cuando el expander está abierto */
    div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
    }

    /* Inputs y botones inferiores */
    input {
        background-color: #2e1a47 !important;
        color: white !important;
        border: 2px solid #f06292 !important;
        text-align: center;
    }

    .stButton>button {
        background: linear-gradient(45deg, #7b1fa2, #f06292);
        color: white !important;
        border: none;
        border-radius: 25px;
        width: 100%;
    }
    
    .centered-text {
        text-align: center;
        color: #fce4ec !important;
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
    # El label ahora es un string simple, el CSS se encarga de pintarlo de blanco
    with st.expander(f"{genero.upper()} {emoji}"):
        user_input = st.text_input(f"¿Cuál es el secreto de {genero}?", key=f"input_{genero}").lower().strip()
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
        <div style="background-color: #2e1a47; border: 3px dashed #f06292; padding: 30px; border-radius: 20px; text-align: center;">
            <h2 style="color: white !important;">¡LOGRADO! ⊹ ࣪ ˖</h2>
            <p style="color: #fce4ec;">Usa el código en tu próxima compra:</p>
            <h1 style="color: #f06292 !important; font-size: 35px;">LECTURA15OFF</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    completados = sum(st.session_state.progreso.values())
    st.progress(completados / 5)
    st.markdown(f'<p class="centered-text">Has encontrado {completados} de 5 secretos.</p>', unsafe_allow_html=True)
