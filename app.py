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

    /* Título optimizado para móvil */
    .main-title {
        text-align: center;
        color: #fff !important;
        font-size: 2.1rem !important;
        font-weight: 600;
        margin-bottom: 25px !important;
        text-shadow: 0 0 10px #b388ff, 0 0 20px #7c4dff;
    }

    /* Expanders (Acordeones) */
    div[data-testid="stExpander"] details summary {
        background-color: #3d1c52 !important; 
        border-radius: 12px !important;
        border: 1px solid #7b1fa2 !important;
        color: #ffffff !important;
        padding: 10px !important;
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
        width: 100%;
    }

    .centered-text {
        text-align: center;
        color: #f3e5f5 !important;
        font-size: 0.85rem;
    }

    .stProgress > div > div > div > div { background-color: #b388ff; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA (AJUSTADA PARA OPENROUTER) ---
def obtener_recomendacion(prompt_usuario, api_key):
    try:
        # Configuración para evitar el Error 401 en OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:8501", 
                "X-Title": "App Biblioteca Magica"
            }
        )
        
        # Usamos un modelo estable de OpenRouter
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un bibliotecario magico. Recomienda un libro breve en espanol sin usar caracteres especiales complejos."},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"El oráculo está nublado: {str(e)}"

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
if 'ia_resp' not in st.session_state:
    st.session_state.ia_resp = None

# --- INTERFAZ ---
st.markdown('<h1 class="main-title">¿Cuándo fue la última vez que leíste?</h1>', unsafe_allow_html=True)

completados = sum(st.session_state.progreso.values())
total = len(RESPUESTAS_CORRECTAS)

if completados < total:
    st.markdown('<p class="centered-text">Descifra los secretos para avanzar.</p>', unsafe_allow_html=True)
    st.progress(completados / total)
    
    rerun_needed = False
    for genero, secreto in RESPUESTAS_CORRECTAS.items():
        status = "✅" if st.session_state.progreso[genero] else "🔍"
        with st.expander(f"{genero.upper()} {status}"):
            if st.session_state.progreso[genero]:
                st.write("✨ Escudo activo.")
            else:
                ans = st.text_input(f"¿Clave de {genero}?", key=f"in_{genero}", label_visibility="collapsed").lower().strip()
                if ans == secreto:
                    st.session_state.progreso[genero] = True
                    rerun_needed = True
    
    if rerun_needed:
        st.rerun()

else:
    if 'globos' not in st.session_state:
        st.balloons()
        st.session_state.globos = True

    # Cuadro de recompensa compacto
    st.markdown("""
        <div style="background-color: #2e1a47; border: 2px dashed #b388ff; padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
            <p style="color: #f3e5f5; font-size: 0.8rem; margin:0;">¡DESAFÍO COMPLETADO!</p>
            <h2 style="color: #b388ff !important; margin:5px 0;">LECTURA15OFF</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="centered-text"><b>Consulta al Oráculo ✨</b></p>', unsafe_allow_html=True)
    
    # API KEY (OpenRouter)
    MI_KEY = "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"
    
    q = st.text_input("¿Qué buscas?", placeholder="Ej: un viaje épico...", label_visibility="collapsed")
    
    if st.button("Consultar"):
        if q:
            with st.spinner("Consultando..."):
                st.session_state.ia_resp = obtener_recomendacion(q, MI_KEY)
        else:
            st.warning("Escribe algo primero.")

    if st.session_state.ia_resp:
        st.info(st.session_state.ia_resp)
