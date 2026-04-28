import streamlit as st
from openai import OpenAI

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS DE PRECISIÓN LILA/AMATISTA ---
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
        text-shadow: 0 0 10px #b388ff, 0 0 20px #b388ff, 0 0 30px #7c4dff;
    }

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

    div[data-testid="stExpander"] details summary:hover {
        background-color: #4a2366 !important;
    }

    .streamlit-expanderContent {
        background-color: #26123d !important;
        border: 1px solid #3d1c52 !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
    }

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
        font-weight: 600;
    }
    
    .centered-text {
        text-align: center;
        color: #f3e5f5 !important;
    }

    .stProgress > div > div > div > div {
        background-color: #b388ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA ---
def obtener_recomendacion(prompt_usuario, api_key):
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un bibliotecario mágico. Recomienda un libro de forma breve y misteriosa."},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"El oráculo está indispuesto... (Error: {e})"

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

completados = sum(st.session_state.progreso.values())
todos_completados = completados == len(RESPUESTAS_CORRECTAS)

if not todos_completados:
    st.markdown('<p class="centered-text">Descubre los secretos ocultos para avanzar.</p>', unsafe_allow_html=True)
    st.progress(completados / len(RESPUESTAS_CORRECTAS))
    st.markdown(f'<p class="centered-text">Has activado {completados} de 5 escudos.</p>', unsafe_allow_html=True)
    st.write("")

    # Variable para controlar si necesitamos recargar la app al final del bucle
    debe_recargar = False

    for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
        # Si ya está completado, mostramos el check, si no, la lupa
        label_emoji = "✅" if st.session_state.progreso[genero] else "🔍"
        
        with st.expander(f"{genero.upper()} {label_emoji}"):
            if st.session_state.progreso[genero]:
                st.write("✨ Este escudo ya está activo.")
            else:
                st.markdown(f'<p style="color: #f3e5f5;">¿Cuál es la palabra secreta de {genero}?</p>', unsafe_allow_html=True)
                # Usamos una clave única y verificamos el cambio
                user_input = st.text_input("", key=f"input_{genero}", label_visibility="collapsed").lower().strip()
                
                if user_input == respuesta_real:
                    st.session_state.progreso[genero] = True
                    debe_recargar = True
                elif user_input != "":
                    st.error("Esa no es la respuesta.")

    if debe_recargar:
        st.rerun()

else:
    st.balloons()
    st.markdown("""
        <div style="background-color: #2e1a47; border: 3px dashed #b388ff; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
            <h2 style="color: white !important;">¡DESAFÍO COMPLETADO! ⊹ ࣪ ˖</h2>
            <p style="color: #f3e5f5;">Tu recompensa es:</p>
            <h1 style="color: #b388ff !important; font-size: 38px; letter-spacing: 4px;">LECTURA15OFF</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="color: #f3e5f5; text-align: center;">El Oráculo de la Biblioteca ✨</h3>', unsafe_allow_html=True)
    
    api_key_final = st.secrets.get("OPENAI_API_KEY", "TU_LLAVE_API_AQUÍ")
    user_query = st.text_input("Describe qué historia buscas...", placeholder="Ej: un viaje épico...")
    
    if st.button("Consultar Oráculo"):
        if not user_query:
            st.warning("Escribe algo para el oráculo.")
        elif api_key_final == "TU_LLAVE_API_AQUÍ":
            st.error("API Key no configurada.")
        else:
            with st.spinner("Consultando pergaminos..."):
                st.info(obtener_recomendacion(user_query, api_key_final))
