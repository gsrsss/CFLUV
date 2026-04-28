import streamlit as st
from openai import OpenAI

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Biblioteca Mágica",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS OPTIMIZADOS (MOBILE FRIENDLY) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #1a0a2e;
    }

    .stApp { background-color: #1a0a2e; }

    /* Título reducido para móviles */
    .main-title {
        text-align: center;
        color: #fff !important;
        font-size: 2.2rem !important; /* Reducido de 3.2rem */
        font-weight: 600;
        margin-bottom: 30px !important;
        text-shadow: 0 0 10px #b388ff, 0 0 20px #7c4dff;
    }

    /* Ajuste de Expanders */
    div[data-testid="stExpander"] details summary {
        background-color: #3d1c52 !important; 
        border-radius: 12px !important;
        border: 1px solid #7b1fa2 !important;
        color: #ffffff !important;
    }

    div[data-testid="stExpander"] details summary p {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background-color: #26123d !important;
        border: 1px solid #3d1c52 !important;
        border-radius: 0 0 12px 12px !important;
    }

    /* Inputs y Botones */
    input {
        background-color: #1a0a2e !important;
        color: #ffffff !important;
        border: 1px solid #7b1fa2 !important;
        border-radius: 10px !important;
    }

    .stButton>button {
        background: linear-gradient(45deg, #6200ea, #b388ff);
        color: white !important;
        border-radius: 20px;
        border: none;
        font-weight: 600;
    }

    .centered-text {
        text-align: center;
        color: #f3e5f5 !important;
        font-size: 0.9rem;
    }

    .stProgress > div > div > div > div { background-color: #b388ff; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA (OPENROUTER) ---
def obtener_recomendacion(prompt_usuario, api_key):
    try:
        # Configuración específica para OpenRouter con tu llave
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", # O usa "google/gemini-2.0-flash-001" si prefieres
            messages=[
                {"role": "system", "content": "Eres un bibliotecario magico. Recomienda un libro en espanol de forma breve."},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en la conexion: {str(e)}"

# --- LÓGICA DE ESTADO ---
RESPUESTAS_CORRECTAS = {
    "Romance": "corazon",
    "Fantasía": "dragon",
    "Ficción": "espejo",
    "No-Ficción": "verdad",
    "Misterio": "llave"
}

if 'progreso' not in st.session_state:
    st.session_state.progreso = {g: False for g in RESPUESTAS_CORRECTAS}
if 'recomendacion_ia' not in st.session_state:
    st.session_state.recomendacion_ia = None

# --- INTERFAZ ---
st.markdown('<h1 class="main-title">¿Cuándo fue la última vez que leíste?</h1>', unsafe_allow_html=True)

completados = sum(st.session_state.progreso.values())
total = len(RESPUESTAS_CORRECTAS)

if completados < total:
    st.markdown('<p class="centered-text">Activa los escudos literarios para continuar.</p>', unsafe_allow_html=True)
    st.progress(completados / total)
    
    debe_recargar = False
    for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
        label = "✅" if st.session_state.progreso[genero] else "🔍"
        with st.expander(f"{genero.upper()} {label}"):
            if st.session_state.progreso[genero]:
                st.write("✨ Escudo activado.")
            else:
                user_input = st.text_input(f"Secreto {genero}", key=f"in_{genero}", label_visibility="collapsed").lower().strip()
                if user_input == respuesta_real:
                    st.session_state.progreso[genero] = True
                    debe_recargar = True
    
    if debe_recargar:
        st.rerun()

else:
    if 'globos' not in st.session_state:
        st.balloons()
        st.session_state.globos = True

    st.markdown("""
        <div style="background-color: #2e1a47; border: 2px dashed #b388ff; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
            <h3 style="color: white !important; margin:0;">¡LOGRADO!</h3>
            <p style="color: #f3e5f5; font-size: 0.9rem;">Usa el código:</p>
            <h2 style="color: #b388ff !important; margin:0;">LECTURA15OFF</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="centered-text"><b>El Oráculo de la Biblioteca ✨</b></p>', unsafe_allow_html=True)
    
    # LLAVE API
    MI_API_KEY = "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"
    
    u_query = st.text_input("¿Qué buscas hoy?", placeholder="Ej: un romance triste...", label_visibility="collapsed")
    
    if st.button("Consultar Oráculo"):
        if u_query:
            with st.spinner("Leyendo pergaminos..."):
                st.session_state.recomendacion_ia = obtener_recomendacion(u_query, MI_API_KEY)
        else:
            st.warning("Escribe algo primero.")

    if st.session_state.recomendacion_ia:
        st.info(st.session_state.recomendacion_ia)
