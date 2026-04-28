import streamlit as st
from openai import OpenAI # O la librería de la IA que prefieras

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

    .main-title {
        text-align: center;
        color: #fff !important;
        font-size: 3.2rem !important;
        font-weight: 600;
        margin-bottom: 50px !important;
        padding-top: 20px;
        text-shadow: 0 0 10px #ff4081, 0 0 20px #ff4081;
    }

    /* Botones de Género Morado Amatista */
    div[data-testid="stExpander"] details summary {
        background-color: #3d1c52 !important; 
        border-radius: 12px !important;
        border: 1px solid #7b1fa2 !important;
        padding: 15px !important;
        color: #ffffff !important;
    }

    div[data-testid="stExpander"] details summary p {
        color: #ffffff !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stExpander"] details summary svg {
        fill: #ffffff !important;
    }

    /* Fix para evitar el fondo blanco en focus */
    div[data-testid="stExpander"] details summary:hover, 
    div[data-testid="stExpander"] details summary:focus {
        background-color: #4a2366 !important;
        color: #ffffff !important;
        outline: none !important;
    }

    .streamlit-expanderContent {
        background-color: #26123d !important;
        border: 1px solid #3d1c52 !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
    }

    /* Inputs y botones */
    input {
        background-color: #1a0a2e !important;
        color: #ffffff !important;
        border: 1px solid #7b1fa2 !important;
        border-radius: 10px !important;
        text-align: center;
    }

    .stButton>button {
        background: linear-gradient(45deg, #7b1fa2, #ff4081);
        color: white !important;
        border-radius: 25px;
        width: 100%;
        border: none;
        font-weight: 600;
    }
    
    .centered-text {
        text-align: center;
        color: #fce4ec !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA ---
def obtener_recomendacion(prompt_usuario, api_key):
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # O el modelo que prefieras
            messages=[
                {"role": "system", "content": "Eres un bibliotecario mágico y misterioso. Recomienda un libro basado en los gustos del usuario de forma breve y encantadora."},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"La biblioteca está cerrada temporalmente... (Error: {e})"

# --- LÓGICA DE PROGRESO ---
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
        st.markdown(f'<p style="color: #fce4ec;">¿Cuál es el secreto de {genero}?</p>', unsafe_allow_html=True)
        user_input = st.text_input("", key=f"input_{genero}", label_visibility="collapsed").lower().strip()
        if user_input == respuesta_real:
            st.session_state.progreso[genero] = True
            st.success("Escudo activado.")

# --- SECCIÓN FINAL / RECOMENDADOR ---
todos_completados = all(st.session_state.progreso.values())

if todos_completados:
    st.divider()
    st.balloons()
    st.markdown("""
        <div style="background-color: #2e1a47; border: 3px dashed #ff4081; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
            <h2 style="color: white !important;">¡LOGRADO! ⊹ ࣪ ˖</h2>
            <p style="color: #fce4ec;">Código de descuento:</p>
            <h1 style="color: #ff80ab !important; font-size: 35px;">LECTURA15OFF</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<h3 style="color: #fce4ec; text-align: center;">Consulta el Oráculo de la Biblioteca ✨</h3>', unsafe_allow_html=True)
    
    # IMPORTANTE: Coloca aquí tu llave o usa st.secrets para mayor seguridad
    mi_api_key = "TU_LLAVE_API_AQUÍ" 
    
    user_query = st.text_input("¿Qué historia buscas hoy?", placeholder="Ej: un romance triste en el espacio...")
    if st.button("Consultar Oráculo"):
        if user_query and mi_api_key != "TU_LLAVE_API_AQUÍ":
            with st.spinner("Buscando en los estantes prohibidos..."):
                respuesta = obtener_recomendacion(user_query, mi_api_key)
                st.info(respuesta)
        else:
            st.warning("Escribe algo para que el oráculo pueda responder (o configura tu API Key).")
else:
    completados = sum(st.session_state.progreso.values())
    st.progress(completados / 5)
    st.markdown(f'<p class="centered-text">Has encontrado {completados} de 5 secretos.</p>', unsafe_allow_html=True)
    st.progress(completados / 5)
    st.markdown(f'<p class="centered-text">Has encontrado {completados} de 5 secretos.</p>', unsafe_allow_html=True)
