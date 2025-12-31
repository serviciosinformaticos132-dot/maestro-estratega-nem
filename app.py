import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de configuración. Contacta a soporte.")

# --- 3. FUNCIONES ---
def registrar_usuario(email, password):
    data = {"email": email, "password": password, "plan": "Gratis", "fecha_registro": str(datetime.now())}
    supabase.table("usuarios").insert(data).execute()

def obtener_usuario(email):
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except: return None

# --- 4. ESTILOS ---
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 40px; background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; border-radius: 15px; margin-bottom: 20px; }
    .price-card { border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-align: center; background-color: #f9f9f9; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVEGACIÓN ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú Principal")
        choice = st.radio("Ir a:", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Adquiere tu licencia y revoluciona tus planeaciones</p></div>", unsafe_allow_html=True)
        st.subheader("Selecciona el plan ideal para ti")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='price-card'><h3>Plan Anual</h3><h2>$899 MXN</h2><p>Acceso completo por 1 año</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='price-card'><h3>Plan 3 Años</h3><h2>$1,999 MXN</h2><p>Ahorro máximo para expertos</p></div>", unsafe_allow_html=True)

    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia y Misión</h1>", unsafe_allow_html=True)
        col_text, col_img = st.columns([1.5, 1])
        with col_text:
            st.markdown("""
            ### ¿Quiénes somos?
            **Maestro Estratega NEM** nació en el corazón de las aulas mexicanas. Entendemos que el tiempo frente al grupo es lo más valioso.
            ### Nuestra Misión
            Democratizar el acceso a la Inteligencia Artificial para todos los docentes de México, facilitando la implementación de la NEM.
            """)
        with col_img:
            st.image("https://images.unsplash.com/photo-1544531585-9847b68c8c86?auto=format&fit=crop&w=500")

    elif choice == "Contacto":
        st.title("📧 Contacto")
        with st.form("contacto"):
            st.text_input("Nombre")
            st.text_area("Mensaje")
            st.form_submit_button("Enviar")

    elif choice == "Registrarse":
        st.subheader("📝 Registro")
        with st.form("reg"):
            email_reg = st.text_input("Correo electrónico")
            pw_reg = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Crear Cuenta"):
                registrar_usuario(email_reg, pw_reg)
                st.success("¡Registrado! Ahora inicia sesión.")

    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso")
        with st.form("login"):
            email_log = st.text_input("Correo")
            pw_log = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(email_log)
                if u and u['password'] == pw_log:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Credenciales incorrectas.")

# --- 6. PANEL DE TRABAJO (SÓLO PARA PAGOS ACTIVOS) ---
else:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.write(f"Maestro: **{st.session_state.user['email']}**")
        st.write(f"Estatus: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    # BLOQUEO POR PLAN GRATIS
    if st.session_state.user['plan'] == "Gratis":
        st.warning("🚨 Tu cuenta está activa pero no tienes una suscripción vigente.")
        st.title("💳 Elige tu Plan para comenzar a planear")
        
        c1, c2 = st.columns(2)
        with c1:
            st.info("### Plan Anual")
            st.write("Acceso a todas las herramientas NEM por 12 meses.")
            st.link_button("Comprar Plan Anual", "https://buy.stripe.com/TU_LINK_AQUI")
        with c2:
            st.success("### Plan 3 Años")
            st.write("La mejor inversión para tu carrera docente.")
            st.link_button("Comprar Plan 3 Años", "https://buy.stripe.com/TU_LINK_OTRO")
        
        st.divider()
        st.write("Una vez realizado el pago, tu cuenta será activada en menos de 24 horas.")
    
    # ACCESO A LA IA (SÓLO SI EL PLAN NO ES GRATIS)
    else:
        st.title("🤖 Estación de Planeación Inteligente")
        tema = st.text_input("Escribe el tema para tu planeación:")
        if st.button("Generar Planeación"):
            with st.spinner("Construyendo..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Experto en NEM genera planeación sobre: {tema}"}]
                    )
                    st.markdown(completion.choices[0].message.content)
                except Exception as e: st.error("Error en IA")

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Venta Autorizada</p></div>", unsafe_allow_html=True)