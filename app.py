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

    /* Título con efecto Neón (Sin tocar, como pediste) */
    .main-title {
        text-align: center;
        color: #fff !important;
        font-size: 3.2rem !important;
        font-weight: 600;
        margin-bottom: 50px !important;
        padding-top: 20px;
        text-shadow: 
            0 0 7px #ff4081,
            0 0 10px #ff4081,
            0 0 21px #ff4081,
            0 0 42px #7b1fa2;
    }

    .centered-text {
        text-align: center;
        color: #fce4ec !important;
        margin-bottom: 30px !important;
    }

    /* --- SOLUCIÓN LEGIBILIDAD BOTONES GÉNERO --- */
    
    /* Forzar el color del texto de la etiqueta del expander */
    .streamlit-expanderHeader p {
        color: #ffffff !important; /* Blanco puro para que se lea siempre */
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderHeader {
        background-color: #d81b60 !important; /* Un rosa más fuerte para contraste */
        border: 2px solid #ff80ab !important;
        border-radius: 12px !important;
        padding: 15px !important;
        opacity: 1 !important;
        margin-bottom: 10px !important;
    }

    /* Flecha del menú en blanco */
    .streamlit-expanderHeader svg {
        fill: #ffffff !important;
    }

    /* Estilo del contenido interior */
    .streamlit-expanderContent {
        background-color: #2e1a47 !important;
        border: 1px solid #d81b60 !important;
        color: white !important;
    }

    /* Estilo de los inputs */
    input {
        background-color: #1a0a2e !important;
        color: white !important;
        border: 1px solid #ff4081 !important;
        border-radius: 10px !important;
        text-align: center;
    }

    /* Botón de Buscar */
    .stButton>button {
        background: linear-gradient(45deg, #7b1fa2, #ff4081);
        color: white !important;
        border-radius: 25px;
        border: none;
        padding: 10px 30px;
        margin: 0 auto;
        display: block;
    }

    /* Barra de progreso */
    .stProgress > div > div > div > div {
        background-color: #ff4081;
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
st.markdown('<h1 class="main-title">¿Cuándo fue la última vez que leíste?</h1>', unsafe_allow_html=True)
st.markdown('<p class="centered-text">Introduce las respuestas que encontraste en los libros para desbloquear un secreto...</p>', unsafe_allow_html=True)

# Géneros
for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
    emoji = "✅" if st.session_state.progreso[genero] else "🔍"
    # Usamos markdown dentro del label para ayudar a la legibilidad si es necesario
    with st.expander(f"{genero.upper()} {emoji}"):
        user_input = st.text_input(f"Secreto de {genero}:", key=f"input_{genero}").lower().strip()
        
        if user_input == respuesta_real:
            st.session_state.progreso[genero] = True
            st.success(f"¡Correcto!")
        elif user_input != "":
            st.error("Sigue buscando...")

# --- RECOMPENSA ---
todos_completados = all(st.session_state.progreso.values())

if todos_completados:
    st.divider()
    st.balloons()
    st.markdown("""
        <div style="background-color: #2e1a47; border: 2px dashed #ff4081; padding: 25px; border-radius: 15px; text-align: center;">
            <h3 style="color: white !important;">¡Felicitaciones! ⊹ ࣪ ˖</h3>
            <p style="color: white;">Desbloqueaste el secreto:</p>
            <div style="font-size: 24px; font-weight: bold; color: #ff80ab;">LECTURA15OFF</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<h3 style="color: white; text-align: center;">¿Cuál será tu próxima lectura? ✨</h3>', unsafe_allow_html=True)
    query = st.text_input("Buscador", placeholder="Ej. misterio y romance...", label_visibility="collapsed")
    if st.button("Buscar"):
        st.info(f"El oráculo sugiere algo basado en tu búsqueda.")
else:
    completados = sum(st.session_state.progreso.values())
    st.progress(completados / 5)
    st.markdown(f'<p class="centered-text">Has desbloqueado {completados} de 5 géneros.</p>', unsafe_allow_html=True)
