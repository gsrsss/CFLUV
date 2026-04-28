import streamlit as st
from openai import OpenAI

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS LILA NEÓN Y AMATISTA ---
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
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700;
        margin-bottom: 30px !important;
        padding-top: 20px;
        text-shadow: 0 0 10px #b388ff, 0 0 20px #7c4dff;
    }

    /* Estilos de los Expanders */
    div[data-testid="stExpander"] details summary {
        background-color: #3d1c52 !important; 
        border-radius: 15px !important;
        border: 2px solid #7b1fa2 !important;
        padding: 15px !important;
        color: #ffffff !important;
    }

    div[data-testid="stExpander"] details summary p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background-color: #26123d !important;
        border: 2px solid #3d1c52 !important;
        border-radius: 0 0 15px 15px !important;
    }

    /* Input y Botones */
    input {
        background-color: #1a0a2e !important;
        color: #ffffff !important;
        border: 1px solid #7b1fa2 !important;
        border-radius: 10px !important;
        text-align: center;
    }

    .stButton>button {
        background: linear-gradient(45deg, #6200ea, #b388ff);
        color: white !important;
        border-radius: 25px;
        width: 100%;
        border: none;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .centered-text {
        text-align: center;
        color: #f3e5f5 !important;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #7c4dff, #b388ff);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA ---
def obtener_recomendacion(prompt_usuario, api_key):
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Biblioteca Magica"
            }
        )
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un bibliotecario magico. Recomienda un libro breve en espanol."},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- LÓGICA DE ESTADO ---
# Se mantiene el progreso del usuario de sesiones anteriores si existen
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
    st.progress(completados / total)
    rerun = False
    for genero, secreto in RESPUESTAS_CORRECTAS.items():
        label = "✅" if st.session_state.progreso[genero] else "🔍"
        with st.expander(f"{genero.upper()} {label}"):
            if st.session_state.progreso[genero]:
                st.write("✨ Escudo activo.")
            else:
                ans = st.text_input(f"Clave {genero}", key=f"in_{genero}", label_visibility="collapsed").lower().strip()
                if ans == secreto:
                    st.session_state.progreso[genero] = True
                    rerun = True
    if rerun: st.rerun()

else:
    if 'globos' not in st.session_state:
        st.balloons()
        st.session_state.globos = True

    # --- CUADRO DE RECOMPENSA (FIJO PARA MÓVIL) ---
    st.markdown(f"""
        <div style="
            background-color: #2e1a47; 
            border: 2px dashed #b388ff; 
            padding: 25px; 
            border-radius: 20px; 
            text-align: center; 
            margin-bottom: 30px;
            box-shadow: 0 0 15px rgba(179, 136, 255, 0.2);
        ">
            <p style="color: #ffffff !important; font-size: 1.2rem; font-weight: 600; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">
                ¡Desafío Completado!
            </p>
            <p style="color: #f3e5f5 !important; font-size: 0.9rem; margin-bottom: 15px;">
                Tu recompensa mágica es:
            </p>
            <h1 style="
                color: #ffffff !important; 
                font-size: 2.2rem !important; 
                font-weight: 700 !important; 
                margin: 0;
                text-shadow: 0 0 10px #b388ff, 0 0 20px #b388ff;
                letter-spacing: 3px;
            ">
                LECTURA15OFF
            </h1>
        </div>
    """, unsafe_allow_html=True)

    # --- SECCIÓN IA ---
    st.markdown('<p class="centered-text"><b>El Oráculo de la Biblioteca ✨</b></p>', unsafe_allow_html=True)
    MI_KEY = "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"
    
    q = st.text_input("¿Qué buscas?", placeholder="Ej: una aventura épica...", label_visibility="collapsed")
    
    if st.button("Consultar Oráculo"):
        if q:
            with st.spinner("Consultando..."):
                st.session_state.ia_resp = obtener_recomendacion(q, MI_KEY)
        else:
            st.warning("Escribe algo primero.")

    if st.session_state.ia_resp:
        st.info(st.session_state.ia_resp)
