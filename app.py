import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS PERSONALIZADOS (Cozy Aesthetic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #FDFBF7; /* Crema suave */
    }

    .stApp {
        background-color: #FDFBF7;
    }

    /* Títulos y texto */
    h1, h2, h3 {
        color: #5D6D7E;
    }

    /* Contenedor del Cupón */
    .coupon-container {
        background-color: #E8F6F3; /* Verde pastel muy suave */
        border: 2px dashed #A9DFBF;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }

    .coupon-code {
        font-size: 24px;
        font-weight: bold;
        color: #2E86C1; /* Azul suave */
        letter-spacing: 2px;
    }

    /* Botones */
    .stButton>button {
        background-color: #FADBD8; /* Rosado pastel */
        color: #444;
        border: none;
        border-radius: 20px;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #F5B7B1;
        transform: scale(1.02);
    }
    
    /* Inputs */
    input {
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
# Definimos las respuestas correctas (Cámbialas por las reales de tus acertijos)
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
st.title("¿Cuándo fue la última vez que leíste?")
st.write("Introduce las respuestas que encontraste en los libros para desbloquear un secreto...")

# Crear columnas para que se vea bien en móvil (layout vertical natural)
for genero, respuesta_real in RESPUESTAS_CORRECTAS.items():
    with st.expander(f"Género: {genero} {'✅' if st.session_state.progreso[genero] else '🔍'}"):
        user_input = st.text_input(f"Respuesta para {genero}:", key=f"input_{genero}").lower().strip()
        
        if user_input == respuesta_real:
            st.session_state.progreso[genero] = True
            st.success(f"¡Correcto! Has encontrado el escudo de {genero}.")
        elif user_input != "":
            st.error("Esa no es la respuesta, ¡sigue buscando en el libro!")

# --- SECCIÓN DE RECOMPENSA ---
todos_completados = all(st.session_state.progreso.values())

if todos_completados:
    st.divider()
    st.balloons()
    st.markdown("""
        <div class="coupon-container">
            <h3>¡Felicitaciones! ⊹ ࣪ ˖</h3>
            <p>Lograste encontrar todos los escudos y responder el acertijo.</p>
            <p>Desbloqueaste el secreto:</p>
            <div class="coupon-code">LECTURA15OFF</div>
            <p><small>Válido para los libros incluidos en la promoción especial.</small></p>
        </div>
    """, unsafe_allow_html=True)

    # --- SECCIÓN DE IA RECOMENDADORA ---
    st.markdown("---")
    st.subheader("Dile al susurrador de libros lo que buscas, y te dirá cuál será tu próxima lectura.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Buscador de libros", placeholder="Ej. quiero un libro de misterio y romance...", label_visibility="collapsed")
    with col2:
        buscar = st.button("Buscar")

    if buscar and query:
        with st.spinner("Consultando con la biblioteca mágica..."):
            # Aquí iría la lógica de conexión con una API de LLM (OpenAI, Anthropic, etc.)
            # Por ahora, simulamos una respuesta:
            st.info(f"Basado en tu búsqueda '{query}', te recomendamos leer **'La Sombra del Viento'** de Carlos Ruiz Zafón.")
else:
    # Barra de progreso visual
    completados = sum(st.session_state.progreso.values())
    st.progress(completados / len(RESPUESTAS_CORRECTAS))
    st.write(f"Has desbloqueado {completados} de {len(RESPUESTAS_CORRECTAS)} géneros.")
