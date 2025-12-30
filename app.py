import streamlit as st
from groq import Groq
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# --- INICIALIZAR FIREBASE ---
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    creds = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(creds)

db = firestore.client()

# --- LÓGICA DE USUARIOS ---
def registrar_usuario(email, password):
    user_ref = db.collection("usuarios").document(email)
    if not user_ref.get().exists:
        user_ref.set({
            "password": password,
            "fecha_registro": datetime.now(),
            "plan": "Trial"
        })
        return True
    return False

def verificar_login(email, password):
    user_ref = db.collection("usuarios").document(email).get()
    if user_ref.exists:
        data = user_ref.to_dict()
        if data["password"] == password:
            return data
    return None

# --- INTERFAZ ---
st.title("🤖 Maestro Estratega NEM Pro")

if 'user' not in st.session_state:
    menu = ["Iniciar Sesión", "Registrarse"]
    choice = st.sidebar.selectbox("Acceso", menu)
    
    email = st.sidebar.text_input("Correo")
    password = st.sidebar.text_input("Contraseña", type="password")

    if choice == "Registrarse":
        if st.sidebar.button("Crear cuenta gratuita (7 días)"):
            if registrar_usuario(email, password):
                st.sidebar.success("¡Cuenta creada! Inicia sesión.")
            else:
                st.sidebar.error("El usuario ya existe.")
    else:
        if st.sidebar.button("Entrar"):
            user_data = verificar_login(email, password)
            if user_data:
                st.session_state.user = user_data
                st.session_state.email = email
                st.rerun()
            else:
                st.sidebar.error("Datos incorrectos.")

# --- CUANDO YA INICIÓ SESIÓN ---
if 'user' in st.session_state:
    # Calcular días
    # Firebase guarda la fecha como objeto, la convertimos
    fecha_reg = st.session_state.user["fecha_registro"]
    # Si viene de Firebase es un objeto datetime, si no, hay que ajustarlo
    try:
        limite = fecha_reg + timedelta(days=7)
    except:
        limite = datetime.now() + timedelta(days=7) # Fallback
        
    dias_restantes = (limite.replace(tzinfo=None) - datetime.now()).days

    if dias_restantes < 0 and st.session_state.user["plan"] == "Trial":
        st.warning("⏳ Tu prueba de 7 días ha terminado.")
        st.subheader("💰 Elige un Plan para continuar")
        col1, col2 = st.columns(2)
        col1.link_button("Plan Anual ($899)", "https://buy.stripe.com/tu_link_1")
        col2.link_button("Plan 3 Años ($1,999)", "https://buy.stripe.com/tu_link_2")
    else:
        st.sidebar.success(f"Días restantes: {max(0, dias_restantes)}")
        if st.sidebar.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()
            
        # --- AQUÍ VA TU CÓDIGO DE LA IA (GROQ) ---
        st.write(f"Bienvenido, maestro/a {st.session_state.email}")
        # (Tu código de planeación aquí...)