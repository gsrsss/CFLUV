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

    /* Título con efecto Neón Rosa */
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
        font-size: 1.1rem;
    }

    /* --- BOTONES DE GÉNERO (EXPANDERS) ROSADOS --- */
    /* Forzamos el color del encabezado del menú desplegable */
    .streamlit-expanderHeader {
        background-color: #f06292 !important; /* Rosa pastel vibrante sólido */
        color: #1a0a2e !important; /* Texto oscuro para máxima legibilidad sobre rosa */
        border-radius: 12px !important;
        border: 2px solid #ff80ab !important;
        padding: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 12px !important;
        font-size: 1.1rem !important;
        opacity: 1 !important; /* Cero transparencia */
    }

    /* Estilo para el contenido de adentro del menú */
    .streamlit-expanderContent {
        background-color: #2e1a47 !important;
        border: 1px solid #f06292 !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
        padding: 20px !important;
    }

    /* Flecha del menú en color oscuro */
    .streamlit-expanderHeader svg {
        fill: #1a0a2e !important;
    }

    /* Botón de Buscar IA */
    .stButton>button {
        background: linear-gradient(45deg, #7b1fa2, #f06292);
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 12px 35px;
        font-weight: 600;
        display: block;
        margin: 0 auto;
        box-shadow: 0 0 10px rgba(240, 98, 146, 0.4);
    }

    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(240, 98, 146, 0.7);
        transform: scale(1.03);
    }

    /* Inputs centrados y claros */
    input {
        background-color: #1a0a2e !important;
        color: white !important;
        border: 1px solid #f06292 !important;
        border-radius: 10px !important;
        text-align: center;
        padding: 10px !important;
    }

    /* Contenedor del Cupón */
    .coupon-container {
        background-color: #2e1a47;
        border: 3px dashed #f06292;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(240, 98, 146, 0.2);
    }

    .coupon-code {
        font-size: 28px;
        font-weight: bold;
        color: #fce4ec;
        text-shadow: 0 0 10px #f06292;
        letter-spacing: 3px;
    }

    /* Barra de progreso rosa */
    .stProgress > div > div > div > div {
        background-color: #f06292;
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

# Listado de géneros con los nuevos botones rosados
for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
    check = "✅" if st.session_state.progreso[genero] else "🔍"
    with st.expander(f"{genero.upper()} {check}"):
        user_input = st.text_input(f"Ingresa el secreto de {genero}:", key=f"input_{genero}").lower().strip()
        
        if user_input == respuesta_real:
            st.session_state.progreso[genero] = True
            st.success(f"¡Logrado! El escudo de {genero} brilla ahora.")
        elif user_input != "":
            st.error("No es la palabra correcta... ¡vuelve al libro!")

# --- SECCIÓN DE RECOMPENSA ---
todos_completados = all(st.session_state.progreso.values())

if todos_completados:
    st.divider()
    st.balloons()
    st.markdown("""
        <div class="coupon-container">
            <h2 style="color: #fff !important; text-align: center;">¡Felicitaciones! ⊹ ࣪ ˖</h2>
            <p>Has unido todos los géneros y completado el desafío.</p>
            <p style="font-style: italic;">Tu secreto es:</p>
            <div class="coupon-code">LECTURA15OFF</div>
            <p><small>Muestra esto en la librería para tu descuento.</small></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="color: #fce4ec !important; text-align: center;">¿Cuál será tu próxima lectura? ✨</h3>', unsafe_allow_html=True)
    
    query = st.text_input("Buscador", placeholder="Ej. quiero un libro de misterio y romance...", label_visibility="collapsed")
    buscar = st.button("Buscar")

    if buscar and query:
        with st.spinner("Consultando la biblioteca..."):
            st.info(f"El destino dice: Para '{query}', tu mejor opción es **'La Sombra del Viento'**.")
else:
    # Barra de progreso y contador
    completados = sum(st.session_state.progreso.values())
    st.markdown(f'<p class="centered-text" style="margin-bottom:5px !important;">Has activado {completados} de 5 escudos</p>', unsafe_allow_html=True)
    st.progress(completados / 5)
