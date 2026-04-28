import streamlit as st
from openai import OpenAI

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS LILA NEÓN Y AMATISTA (DISEÑO COMPLETO) ---
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

    /* Título con brillo Neón Lila Potente */
    .main-title {
        text-align: center;
        color: #fff !important;
        font-size: 3rem !important;
        font-weight: 700;
        margin-bottom: 40px !important;
        padding-top: 20px;
        text-shadow: 
            0 0 10px #b388ff, 
            0 0 20px #b388ff, 
            0 0 40px #7c4dff,
            0 0 70px #7c4dff;
    }

    /* Botones de Género (Expanders Amatista) */
    div[data-testid="stExpander"] details summary {
        background-color: #3d1c52 !important; 
        border-radius: 15px !important;
        border: 2px solid #7b1fa2 !important;
        padding: 18px !important;
        color: #ffffff !important;
        transition: 0.3s;
    }

    div[data-testid="stExpander"] details summary p {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stExpander"] details summary:hover {
        background-color: #4a2366 !important;
        border-color: #b388ff !important;
        box-shadow: 0 0 15px rgba(179, 136, 255, 0.4);
    }

    .streamlit-expanderContent {
        background-color: #26123d !important;
        border: 2px solid #3d1c52 !important;
        border-top: none !important;
        border-bottom-left-radius: 15px !important;
        border-bottom-right-radius: 15px !important;
        padding: 20px !important;
    }

    /* Inputs y Texto */
    input {
        background-color: #1a0a2e !important;
        color: #ffffff !important;
        border: 1px solid #7b1fa2 !important;
        border-radius: 12px !important;
        text-align: center;
        font-size: 1.1rem !important;
    }

    /* Botón de Consultar Oráculo */
    .stButton>button {
        background: linear-gradient(45deg, #6200ea, #b388ff);
        color: white !important;
        border-radius: 30px;
        width: 100%;
        border: none;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 10px;
        transition: 0.4s;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton>button:hover {
        box-shadow: 0 0 25px #b388ff;
        transform: scale(1.02);
    }
    
    .centered-text {
        text-align: center;
        color: #f3e5f5 !important;
        font-weight: 400;
    }

    /* Barra de progreso personalizada */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #7c4dff, #b388ff);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA (OPENROUTER FIX 401) ---
def obtener_recomendacion(prompt_usuario, api_key):
    try:
        # Headers necesarios para OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Biblioteca Magica Pro"
            }
        )
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un bibliotecario magico. Recomienda un libro de forma breve, misteriosa y encantadora en español."},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"✨ El oráculo susurra un error: {str(e)}"

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
if 'ia_resp' not in st.session_state:
    st.session_state.ia_resp = None

# --- INTERFAZ ---
st.markdown('<h1 class="main-title">¿Cuándo fue la última vez que leíste?</h1>', unsafe_allow_html=True)

completados = sum(st.session_state.progreso.values())
todos_completados = completados == len(RESPUESTAS_CORRECTAS)

if not todos_completados:
    st.markdown('<p class="centered-text">Descubre los secretos ocultos para activar los escudos de amatista.</p>', unsafe_allow_html=True)
    st.progress(completados / len(RESPUESTAS_CORRECTAS))
    st.markdown(f'<p class="centered-text">Has activado {completados} de 5 escudos.</p>', unsafe_allow_html=True)
    st.write("")

    rerun = False
    for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
        label = "✅" if st.session_state.progreso[genero] else "🔍"
        with st.expander(f"{genero.upper()} {label}"):
            if st.session_state.progreso[genero]:
                st.write("✨ Este escudo brilla con luz propia.")
            else:
                st.markdown(f'<p style="color: #f3e5f5;">¿Cuál es el secreto de {genero}?</p>', unsafe_allow_html=True)
                user_input = st.text_input("", key=f"input_{genero}", label_visibility="collapsed").lower().strip()
                if user_input == respuesta_real:
                    st.session_state.progreso[genero] = True
                    rerun = True
    if rerun:
        st.rerun()

else:
    if 'globos' not in st.session_state:
        st.balloons()
        st.session_state.globos = True

    # Cuadro de recompensa estético
    st.markdown("""
        <div style="background-color: #2e1a47; border: 3px dashed #b388ff; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 40px; box-shadow: 0 0 20px rgba(179, 136, 255, 0.3);">
            <h2 style="color: white !important; letter-spacing: 2px;">¡DESAFÍO COMPLETADO!</h2>
            <p style="color: #f3e5f5;">Tu recompensa mágica es:</p>
            <h1 style="color: #b388ff !important; font-size: 45px; text-shadow: 0 0 10px #b388ff;">LECTURA15OFF</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<h3 style="color: #f3e5f5; text-align: center;">El Oráculo de la Biblioteca ✨</h3>', unsafe_allow_html=True)
    
    # LLAVE API OPENROUTER
    MI_API_KEY = "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"
    
    user_query = st.text_input("¿Qué historia buscas hoy?", placeholder="Ej: un viaje épico hacia lo desconocido...")
    
    if st.button("Consultar Oráculo"):
        if user_query:
            with st.spinner("Consultando los pergaminos antiguos..."):
                st.session_state.ia_resp = obtener_recomendacion(user_query, MI_API_KEY)
        else:
            st.warning("El oráculo necesita palabras para despertar.")

    if st.session_state.ia_resp:
        st.markdown(f"""
            <div style="background-color: #1a0a2e; border: 1px solid #7c4dff; padding: 20px; border-radius: 15px; color: #f3e5f5; margin-top: 20px;">
                {st.session_state.ia_resp}
            </div>
        """, unsafe_allow_html=True)
