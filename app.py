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
        color: #fff !important;
        font-size: 3.2rem !important;
        font-weight: 600;
        margin-bottom: 50px !important;
        padding-top: 20px;
        text-shadow: 0 0 10px #b388ff, 0 0 20px #b388ff, 0 0 35px #7c4dff;
    }

    /* Estilo de los botones de género (Expanders) */
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

    div[data-testid="stExpander"] details summary:hover {
        background-color: #4a2366 !important;
    }

    .streamlit-expanderContent {
        background-color: #26123d !important;
        border: 1px solid #3d1c52 !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
    }

    /* Estilo de los Inputs */
    input {
        background-color: #1a0a2e !important;
        color: #ffffff !important;
        border: 1px solid #7b1fa2 !important;
        border-radius: 10px !important;
        text-align: center;
    }

    /* Botón de acción */
    .stButton>button {
        background: linear-gradient(45deg, #6200ea, #b388ff);
        color: white !important;
        border-radius: 25px;
        width: 100%;
        border: none;
        font-weight: 600;
    }

    /* Barra de progreso Lila */
    .stProgress > div > div > div > div {
        background-color: #b388ff;
    }
    
    .centered-text {
        text-align: center;
        color: #f3e5f5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA (CON FIX DE ENCODING) ---
def obtener_recomendacion(prompt_usuario, api_key):
    try:
        client = OpenAI(api_key=api_key)
        # Forzamos una respuesta simple y clara para evitar errores de codificación del sistema local
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un bibliotecario magico. Recomienda un libro de forma breve y encantadora en espanol. No uses caracteres especiales complejos."},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        # Mensaje de error simplificado sin caracteres que rompan el codec ASCII
        return "El oraculo tiene problemas con los pergaminos antiguos. Intenta con una descripcion simple."

# --- LÓGICA DE ESTADO (Session State) ---
RESPUESTAS_CORRECTAS = {
    "Romance": "corazon",
    "Fantasía": "dragon",
    "Ficción": "espejo",
    "No-Ficción": "verdad",
    "Misterio": "llave"
}

if 'progreso' not in st.session_state:
    st.session_state.progreso = {genero: False for genero in RESPUESTAS_CORRECTAS}

if 'recomendacion_ia' not in st.session_state:
    st.session_state.recomendacion_ia = None

# --- INTERFAZ PRINCIPAL ---
st.markdown('<h1 class="main-title">¿Cuándo fue la última vez que leíste?</h1>', unsafe_allow_html=True)

completados = sum(st.session_state.progreso.values())
todos_completados = completados == len(RESPUESTAS_CORRECTAS)

if not todos_completados:
    st.markdown('<p class="centered-text">Escribe la respuesta correcta para activar cada escudo literario.</p>', unsafe_allow_html=True)
    st.progress(completados / len(RESPUESTAS_CORRECTAS))
    st.markdown(f'<p class="centered-text">Has activado {completados} de 5 escudos.</p>', unsafe_allow_html=True)
    
    debe_recargar = False
    for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
        label_emoji = "✅" if st.session_state.progreso[genero] else "🔍"
        with st.expander(f"{genero.upper()} {label_emoji}"):
            if st.session_state.progreso[genero]:
                st.write("✨ Este escudo ya brilla con fuerza.")
            else:
                st.markdown(f'<p style="color: #f3e5f5;">Cual es el secreto de {genero}?</p>', unsafe_allow_html=True)
                user_input = st.text_input("", key=f"input_{genero}", label_visibility="collapsed").lower().strip()
                if user_input == respuesta_real:
                    st.session_state.progreso[genero] = True
                    debe_recargar = True
    if debe_recargar:
        st.rerun()

# --- SECCIÓN FINAL: RECOMPENSA E IA ---
else:
    if 'globos_mostrados' not in st.session_state:
        st.balloons()
        st.session_state.globos_mostrados = True

    st.markdown("""
        <div style="background-color: #2e1a47; border: 3px dashed #b388ff; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
            <h2 style="color: white !important;">¡DESAFÍO COMPLETADO! ⊹ ࣪ ˖</h2>
            <p style="color: #f3e5f5;">Tu recompensa por ser un gran lector es:</p>
            <h1 style="color: #b388ff !important; font-size: 38px; letter-spacing: 4px;">LECTURA15OFF</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="color: #f3e5f5; text-align: center;">El Oráculo de la Biblioteca ✨</h3>', unsafe_allow_html=True)
    
    # PEGA TU LLAVE AQUÍ
    MI_API_KEY = "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" 
    
    user_query = st.text_input("Describe que historia buscas hoy...", placeholder="Ej: un viaje epico...")
    
    if st.button("Consultar Oráculo"):
        if not user_query:
            st.warning("El oraculo necesita palabras para funcionar.")
        elif MI_API_KEY == "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":
            st.error("Configura la API Key para activar la magia.")
        else:
            with st.spinner("Consultando los pergaminos..."):
                st.session_state.recomendacion_ia = obtener_recomendacion(user_query, MI_API_KEY)

    # Mostrar la recomendación si existe en el estado
    if st.session_state.recomendacion_ia:
        st.info(st.session_state.recomendacion_ia)
