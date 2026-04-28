import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="¿Cuándo fue la última vez que leíste?",
    page_icon="📖",
    layout="centered"
)

# --- ESTILOS PERSONALIZADOS (Estética Mágica con Estrellas) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;600&display=swap');

    /* Fondo Base */
    .stApp {
        background-color: #1a0a2e;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px),
            radial-gradient(rgba(255,255,255,.4), rgba(255,255,255,.1) 2px, transparent 30px);
        background-size: 550px 550px, 350px 350px, 250px 250px, 150px 150px;
        background-position: 0 0, 40px 60px, 130px 270px, 70px 100px;
    }

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }

    /* Títulos y texto */
    h1, h2, h3, p, span, label {
        color: #fce4ec !important;
        text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.2);
    }

    /* Estilo para los Expanders (Acordeones) */
    .streamlit-expanderHeader {
        background-color: rgba(61, 28, 82, 0.8) !important; /* Semi-transparente para ver estrellas */
        border: 1px solid #7b1fa2 !important;
        border-radius: 10px !important;
        color: #ff80ab !important;
    }

    /* Contenedor del Cupón */
    .coupon-container {
        background-color: rgba(46, 26, 71, 0.9);
        border: 2px dashed #ff4081;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0px 0px 20px rgba(255, 64, 129, 0.4);
    }

    .coupon-code {
        font-size: 26px;
