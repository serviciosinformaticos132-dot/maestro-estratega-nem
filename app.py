import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #555;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #ddd;
        font-size: 14px;
    }
    .hero-text {
        text-align: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENÚ SUPERIOR (Navegación) ---
# Usamos un selectbox horizontal o radio buttons con estilo de menú
menu = ["Inicio", "Registrarse", "Iniciar Sesión"]
choice = st.sidebar.radio("Navegación Principal", menu)

# --- SECCIÓN: INICIO (Landing Page con pasarela) ---
if choice == "Inicio":
    st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><h3>La inteligencia artificial que planea por ti.</h3></div>", unsafe_allow_html=True)
    
    # Pasarela de imágenes (Carrusel simple)
    # Streamlit no tiene carrusel nativo, pero podemos usar columnas o st.image con un loop
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=800", caption="Innovación Educativa")
    
    st.divider()
    
    # Sección de Videos Informativos
    st.subheader("📺 ¿Cómo funciona?")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Reemplaza con tu video tutorial
    with v_col2:
        st.markdown("""
        ### Beneficios:
        * Planeaciones alineadas a la NEM 2022.
        * Sugerencias de libros de texto SEP.
        * Generación de rúbricas y exámenes en segundos.
        * **7 días de prueba totalmente gratis.**
        """)

# --- SECCIÓN: REGISTRO E INICIO DE SESIÓN ---
elif choice == "Registrarse":
    st.subheader("📝 Crear cuenta nueva")
    # ... Aquí va tu lógica de Supabase para registrar ...
    st.info("Regístrate hoy y obtén 7 días de acceso Premium.")

elif choice == "Iniciar Sesión":
    st.subheader("🔑 Acceso para Maestros")
    # ... Aquí va tu lógica de login con Supabase ...

# --- PIE DE PÁGINA (Footer) ---
st.markdown("""
    <div class="footer">
        <p>© 2025 Maestro Estratega NEM - Todos los derechos reservados. | 
        <a href="#">Términos y Condiciones</a> | 
        <a href="#">Contacto</a></p>
    </div>
    """, unsafe_allow_html=True)