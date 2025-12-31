import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de configuración de Base de Datos. Revisa los Secrets.")

# --- 3. FUNCIONES DE LÓGICA ---
def registrar_usuario(email, password, plan_elegido="Gratis"):
    try:
        data = {
            "email": str(email), 
            "password": str(password), 
            "plan": plan_elegido, 
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        supabase.table("usuarios").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error al registrar: {e}")
        return False

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
    .price-card-selected { border: 2px solid #3b82f6; padding: 25px; border-radius: 15px; text-align: center; background-color: #ffffff; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px; }
    .payment-box { background-color: #f1f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-top: 10px; }
    .floating-menu { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6; box-shadow: 0px 10px 30px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVEGACIÓN (NO LOGUEADO) ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["📊 Planeación", "📝 Evaluación", "🖍️ Materiales"])
        with t1: st.image("https://via.placeholder.com/1200x400.png?text=Planeaciones+Alineadas+a+la+NEM", use_container_width=True)
        with t2: st.image("https://via.placeholder.com/1200x400.png?text=Rubricas+y+Examenes", use_container_width=True)
        with t3: st.image("https://via.placeholder.com/1200x400.png?text=Sugerencias+de+Libros+SEP", use_container_width=True)
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia y Misión</h1>", unsafe_allow_html=True)
        ca1, ca2 = st.columns([1.5, 1])
        with ca1: st.markdown("Maestro Estratega NEM nació para reducir la carga administrativa docente...")
        with ca2: st.image("https://images.unsplash.com/photo-1544531585-9847b68c8c86?auto=format&fit=crop&w=500")

    elif choice == "Contacto":
        st.title("📧 Contacto")
        with st.form("contacto"):
            st.text_input("Nombre"); st.text_input("Email"); st.text_area("Mensaje")
            if st.form_submit_button("Enviar"): st.success("Enviado")

    elif choice == "Registrarse":
        st.subheader("📝 Crear Cuenta")
        with st.form("reg_principal"):
            email_reg = st.text_input("Correo electrónico")
            pw_reg = st.text_input("Contraseña", type="password")
            btn_reg = st.form_submit_button("Siguiente paso")
            
            if btn_reg:
                if email_reg and pw_reg:
                    st.session_state['temp_email'] = email_reg
                    st.session_state['temp_pw'] = pw_reg
                    st.session_state['show_options'] = True
                else: st.error("Completa los campos.")

        if st.session_state.get('show_options'):
            st.markdown("<div class='floating-menu'>", unsafe_allow_html=True)
            st.markdown("### 🎯 Elige cómo quieres empezar:")
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            
            with col_opt1:
                if st.button("🎁 Versión de Prueba (Gratis)", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Prueba"):
                        st.success("¡Cuenta de Prueba activada! Inicia Sesión.")
            
            with col_opt2:
                if st.button("📅 Plan Anual ($899)", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Gratis"):
                        st.info("Cuenta creada. Realiza tu pago al iniciar sesión.")
            
            with col_opt3:
                if st.button("💎 Plan 3 Años ($1,999)", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Gratis"):
                        st.info("Cuenta creada. Realiza tu pago al iniciar sesión.")
            st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso")
        with st.form("login"):
            e_log = st.text_input("Email")
            p_log = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(e_log)
                if u and u['password'] == p_log:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Error de acceso.")

# --- 6. PANEL DE CONTROL (LOGUEADO) ---
else:
    with st.sidebar:
        st.write(f"Estatus: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    # --- LÓGICA DE ACCESO POR PLAN ---
    plan = st.session_state.user['plan']

    if plan == "Gratis":
        st.title("💳 Activa tu Suscripción")
        cp1, cp2 = st.columns(2)
        with cp1:
            st.markdown("<div class='price-card-selected'><h3>ANUAL</h3><h1>$899</h1></div>", unsafe_allow_html=True)
            with st.expander("Pagar Plan Anual"):
                st.link_button("Tarjeta", "https://buy.stripe.com/LINK1")
        with cp2:
            st.markdown("<div class='price-card-selected'><h3>3 AÑOS</h3><h1>$1,999</h1></div>", unsafe_allow_html=True)
            with st.expander("Pagar Plan 3 Años"):
                st.link_button("PayPal", "https://paypal.me/LINK2")
                st.markdown("<div class='payment-box'>CLABE: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)

    elif plan == "Prueba":
        st.title("🎁 Modo de Prueba (Limitado)")
        st.info("Esta es una versión limitada para que conozcas la IA.")
        tema = st.text_input("Tema de prueba:")
        if st.button("Generar Planeación Corta"):
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":f"Resumen corto NEM: {tema}"}])
            st.markdown(res.choices[0].message.content)

    elif plan in ["Anual", "Premium", "3 Años"]:
        st.title("🤖 Generador de Planeación Profesional")
        tema = st.text_input("Tema completo:")
        if st.button("Generar Planeación"):
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Planeación detallada NEM: {tema}"}])
            st.markdown(res.choices[0].message.content)

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM</p></div>", unsafe_allow_html=True)