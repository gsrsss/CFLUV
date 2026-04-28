import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS PERSONALIZADOS (Dark Cozy Aesthetic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;600&display=swap');

    /* Fondo principal y fuentes */
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #1E1E1E; /* Negro café oscuro */
        color: #EAE2D6; /* Texto crema claro para contraste */
    }

    .stApp {
        background-color: #262220; /* Tono chocolate oscuro */
    }

    /* Títulos con un toque dorado/cálido */
    h1, h2, h3 {
        color: #D4AC0D !important; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Texto general */
    .stMarkdown p {
        color: #D5DBDB;
    }

    /* Estilo para los Expanders (Acordeones) */
    .streamlit-expanderHeader {
        background-color: #383431 !important;
        border-radius: 10px !important;
        color: #FADBD8 !important; /* Acento rosado suave */
    }

    /* Contenedor del Cupón - Estilo Mágico */
    .coupon-container {
        background-color: #2D3E33; /* Verde bosque oscuro */
        border: 2px dashed #A9DFBF;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    }

    .coupon-code {
        font-size: 28px;
        font-weight: bold;
        color: #AED6F1; /* Azul pastel brillante */
        letter-spacing: 4px;
        margin: 15px 0;
    }

    /* Botones con acento cálido */
    .stButton>button {
        background-color: #E67E22; /* Naranja cálido/quemado */
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #D35400;
        transform: translateY(-2px);
        box-shadow: 0px 5px 10px rgba(0,0,0,0.3);
    }
    
    /* Inputs y áreas de texto */
    input {
        background-color: #3D3835 !important;
        color: white !important;
        border: 1px solid #5D6D7E !important;
        border-radius: 12px !important;
    }

    /* Ajuste para móvil */
    @media (max-width: 640px) {
        .coupon-code {
            font-size: 20px;
        }
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
st.title("🍂 ¿Cuándo fue la última vez que leíste?")
st.write("Introduce las respuestas de los acertijos ocultos en los libros para desbloquear el secreto de la librería.")

# Iteración de géneros
for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
    check = "✅" if st.session_state.progreso[genero] else "📖"
    with st.expander(f"{check} Género: {genero}"):
        user_input = st.text_input(f"Escribe la respuesta de {genero}:", key=f"input_{genero}").lower().strip()
        
        if user_input == respuesta_real:
            st.session_state.progreso[genero] = True
            st.success(f"¡Correcto! El escudo de {genero} ha sido activado.")
        elif user_input != "":
            st.warning("Esa palabra no abre este secreto... intenta de nuevo.")

# --- SECCIÓN DE RECOMPENSA ---
todos_completados = all(st.session_state.progreso.values())

if todos_completados:
    st.divider()
    st.balloons()
    st.markdown("""
        <div class="coupon-container">
            <h2 style="color: #FADBD8 !important;">¡Felicitaciones! ⊹ ࣪ ˖</h2>
            <p style="color: #EAE2D6;">Has demostrado ser un lector excepcional. Has reunido todos los escudos.</p>
            <p style="color: #EAE2D6; font-style: italic;">Tu recompensa secreta es:</p>
            <div class="coupon-code">LECTURA15OFF</div>
            <p style="font-size: 0.8em; color: #A9DFBF;">Muestra este código en caja para un 15% de descuento en la selección del proyecto.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- SECCIÓN DE IA RECOMENDADORA ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("✨ Obten tu próxima recomendación lectora aquí!")
    st.write("Cuéntale a la biblioteca mágica qué buscas...")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Buscador", placeholder="Ej. quiero un libro de misterio y romance...", label_visibility="collapsed")
    with col2:
        buscar = st.button("Buscar")

    if buscar and query:
        with st.spinner("Consultando los archivos mágicos..."):
            # Simulación de respuesta IA
            st.info(f"El oráculo literario sugiere: Basado en '{query}', deberías explorar **'La Sombra del Viento'**.")
else:
    # Barra de progreso estilizada
    completados = sum(st.session_state.progreso.values())
    st.write(f"Progreso de búsqueda: {completados}/5 escudos encontrados")
    st.progress(completados / len(RESPUESTAS_CORRECTAS))
