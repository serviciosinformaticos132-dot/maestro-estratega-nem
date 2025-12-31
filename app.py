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

# --- 3. FUNCIONES DE LÓGICA ---
def registrar_usuario(email, password):
    data = {"email": email, "password": password, "plan": "Gratis", "fecha_registro": str(datetime.now())}
    supabase.table("usuarios").insert(data).execute()
    # Guardamos en la sesión que es un registro nuevo para mostrar bienvenida
    st.session_state['registro_exitoso'] = True

def obtener_usuario(email):
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except: return None

# --- 4. ESTILOS CSS ---
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 40px; background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; border-radius: 15px; margin-bottom: 20px; }
    .price-card-selected { border: 2px solid #3b82f6; padding: 25px; border-radius: 15px; text-align: center; background-color: #ffffff; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px; }
    .payment-box { background-color: #f1f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-top: 10px; }
    .welcome-card { background-color: #e8f5e9; border: 1px solid #2e7d32; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE NAVEGACIÓN ---
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
            st.markdown("<div class='price-card-selected'><h3>Plan Anual</h3><h2>$899 MXN</h2><p>Acceso completo por 1 año</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='price-card-selected'><h3>Plan 3 Años</h3><h2>$1,999 MXN</h2><p>Ahorro máximo para expertos</p></div>", unsafe_allow_html=True)

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
        st.title("📧 Contacto y Soporte")
        st.write("Envía aquí tu comprobante de pago o dudas técnicas.")
        with st.form("contacto"):
            st.text_input("Nombre")
            st.text_input("Correo electrónico")
            st.text_area("Mensaje o ID de transacción")
            st.form_submit_button("Enviar Mensaje")

    elif choice == "Registrarse":
        st.subheader("📝 Registro de Usuario")
        if st.session_state.get('registro_exitoso'):
            st.markdown("""
            <div class='welcome-card'>
            <h3>🎉 ¡Registro exitoso!</h3>
            <p>Tu cuenta ha sido creada. Para activar tu acceso Premium, por favor realiza tu pago e <b>Inicia Sesión</b>.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("reg"):
            email_reg = st.text_input("Correo electrónico")
            pw_reg = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Crear Cuenta"):
                registrar_usuario(email_reg, pw_reg)
                st.rerun()

    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso al Panel")
        with st.form("login"):
            email_log = st.text_input("Correo")
            pw_log = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(email_log)
                if u and u['password'] == pw_log:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Credenciales incorrectas.")

# --- 6. PANEL DE TRABAJO ---
else:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.write(f"Maestro: **{st.session_state.user['email']}**")
        st.write(f"Estatus: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    if st.session_state.user['plan'] == "Gratis":
        st.warning("🚨 Cuenta pendiente de activación.")
        st.title("💎 Activa tu Suscripción")
        
        # Mensaje de bienvenida post-login para nuevos
        st.markdown(f"""
        ### ¡Hola, Maestro/a!
        Gracias por registrarte en **Maestro Estratega NEM**. Para comenzar a generar tus planeaciones alineadas a la NEM, elige una de las siguientes opciones de pago:
        """)

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("<div class='price-card-selected'><h3>PLAN ANUAL</h3><h1>$899</h1><small>MXN / Año</small></div>", unsafe_allow_html=True)
            with st.expander("💳 PAGAR AHORA"):
                st.write("**Opción A: Automático**")
                st.link_button("Tarjeta Crédito/Débito", "https://buy.stripe.com/TU_LINK", use_container_width=True)
                st.write("**Opción B: Manual**")
                st.markdown("<div class='payment-box'><strong>Banco:</strong> BBVA<br><strong>CLABE:</strong> 0123 4567 8901 2345 67<br><strong>Beneficiario:</strong> Tu Nombre</div>", unsafe_allow_html=True)

        with col_p2:
            st.markdown("<div class='price-card-selected'><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1><small>MXN / Total</small></div>", unsafe_allow_html=True)
            with st.expander("💳 PAGAR AHORA"):
                st.link_button("Pagar con PayPal", "https://paypal.me/tuusuario", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>SPEI:</strong> 0123 4567 8901 2345 67<br><strong>Concepto:</strong> Licencia 3 Años</div>", unsafe_allow_html=True)

        st.info("📩 Una vez hecho el pago, tu cuenta se activará automáticamente (Stripe) o manualmente enviando tu ticket a la sección de 'Contacto'.")
    
    else:
        # EL MOTOR DE IA (SÓLO PARA PAGADOS)
        st.title("🤖 Estación de Planeación Inteligente")
        tema = st.text_input("Escribe el contenido o PDA a planear:")
        if st.button("Generar Planeación Completa"):
            with st.spinner("Construyendo planeación pedagógica..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Genera una planeación NEM detallada sobre: {tema}"}]
                    )
                    st.markdown(completion.choices[0].message.content)
                except Exception as e: st.error("Error en conexión con la IA.")

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Matamoros, Tam. | Soporte: contacto@tuapp.com</p></div>", unsafe_allow_html=True)