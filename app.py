import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
# Si falla aquí, es por los Secrets de Streamlit
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de conexión con la base de datos. Verifica tus Secrets.")

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
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except:
        return None

# --- 4. ESTILOS CSS ---
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 40px; background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; border-radius: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE NAVEGACIÓN ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])
    
    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>IA para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        st.subheader("📸 Conoce nuestras herramientas")
        t1, t2 = st.tabs(["🚀 Galería", "📺 Video"])
        with t1: st.image("https://via.placeholder.com/1000x400?text=Bienvenido+Maestro")
        with t2: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia</h1>", unsafe_allow_html=True)
        st.write("**Maestro Estratega NEM** nació para reducir la carga administrativa docente.")

    elif choice == "Contacto":
        st.title("📧 Contacto")
        with st.form("contacto"):
            nombre = st.text_input("Nombre")
            if st.form_submit_button("Enviar"): st.success("Mensaje recibido.")

    elif choice == "Registrarse":
        st.subheader("📝 Registro")
        with st.form("reg"):
            email = st.text_input("Email")
            pw = st.text_input("Pass", type="password")
            cpw = st.text_input("Confirm", type="password")
            if st.form_submit_button("Crear Cuenta"):
                if pw == cpw:
                    registrar_usuario(email, pw)
                    st.success("¡Registrado! Ve a Iniciar Sesión.")
                else: st.error("Las contraseñas no coinciden.")

    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso")
        with st.form("login"):
            email = st.text_input("Email")
            pw = st.text_input("Pass", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(email)
                if u and u['password'] == pw:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Error de acceso.")

else:
    # PANEL DE TRABAJO
    with st.sidebar:
        st.image("logo.png", width=150)
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    st.title("🤖 Estación de Planeación")
    tema = st.text_input("Tema:")
    if st.button("Generar"):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":tema}])
        st.markdown(res.choices[0].message.content)

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM</p></div>", unsafe_allow_html=True)