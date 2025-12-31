import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS (SUPABASE) ---
# Estos datos deben estar en Settings > Secrets de Streamlit
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- 3. FUNCIONES DE LÓGICA ---
def registrar_usuario(email, password):
    data = {
        "email": email, 
        "password": password, 
        "plan": "Gratis", 
        "fecha_registro": str(datetime.now())
    }
    supabase.table("usuarios").insert(data).execute()

def obtener_usuario(email):
    res = supabase.table("usuarios").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None

# --- 4. ESTILOS CSS ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #ddd;
        font-size: 14px;
        z-index: 100;
    }
    .hero-text {
        text-align: center;
        padding: 40px;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MENÚ DE NAVEGACIÓN ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])
    
    # --- SECCIÓN: INICIO ---
    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>IA para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        st.write("### 📸 Galería de Funciones")
        t1, t2 = st.tabs(["Planeación", "Videos"])
        with t1:
            st.image("https://via.placeholder.com/1000x400?text=Pasarela+de+Imagenes+Aqui")
        with t2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # --- SECCIÓN: ACERCA DE ---
    elif choice == "Acerca de":
        st.title("📖 Sobre Nosotros")
        st.write("Somos una plataforma dedicada a simplificar la labor docente mediante IA.")

    # --- SECCIÓN: CONTACTO ---
    elif choice == "Contacto":
        st.title("📧 Contacto")
        with st.form("contacto"):
            nombre = st.text_input("Nombre")
            mensaje = st.text_area("Mensaje")
            if st.form_submit_button("Enviar"):
                st.success("¡Gracias! Te contactaremos pronto.")

    # --- SECCIÓN: REGISTRO ---
    elif choice == "Registrarse":
        st.subheader("📝 Crear cuenta")
        with st.form("reg"):
            email = st.text_input("Email")
            pw = st.text_input("Contraseña", type="password")
            confirm = st.text_input("Confirmar Contraseña", type="password")
            if st.form_submit_button("Registrar"):
                if pw == confirm:
                    registrar_usuario(email, pw)
                    st.success("Usuario creado. Ahora inicia sesión.")
                else: st.error("Las contraseñas no coinciden.")

    # --- SECCIÓN: LOGIN ---
    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso")
        with st.form("login"):
            email = st.text_input("Email")
            pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(email)
                if u and u['password'] == pw:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Error en credenciales.")

# --- 6. PANEL DE TRABAJO (SOLO SI ESTÁ LOGUEADO) ---
else:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.write(f"Maestro: **{st.session_state.user['email']}**")
        st.write(f"Plan: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    st.title("🤖 Estación de Planeación")
    tema = st.text_input("Escribe el tema para tu planeación:")
    if st.button("Generar Planeación con IA"):
        with st.spinner("La IA está trabajando..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Genera una planeación NEM sobre: {tema}"}]
                )
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error con la IA: {e}")

# --- 7. PIE DE PÁGINA ---
st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM</p></div>", unsafe_allow_html=True)