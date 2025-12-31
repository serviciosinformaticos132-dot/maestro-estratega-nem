import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS (SUPABASE) ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de configuración de Base de Datos. Revisa los Secrets.")

# --- 3. FUNCIONES DE LÓGICA ---
def registrar_usuario(email, password):
    data = {"email": email, "password": password, "plan": "Gratis", "fecha_registro": str(datetime.now())}
    supabase.table("usuarios").insert(data).execute()
    st.session_state['registro_exitoso'] = True

def obtener_usuario(email):
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except: return None

# --- 4. ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 40px; background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; border-radius: 15px; margin-bottom: 20px; }
    .price-card-selected { border: 2px solid #3b82f6; padding: 25px; border-radius: 15px; text-align: center; background-color: #ffffff; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px; }
    .payment-box { background-color: #f1f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-top: 10px; font-family: monospace; }
    .welcome-card { background-color: #e8f5e9; border: 1px solid #2e7d32; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE NAVEGACIÓN (USUARIO NO LOGUEADO) ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150) # Asegúrate de tener logo.png en GitHub
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])
        st.divider()
        st.info("Apoyando la labor docente en México.")

    # --- SECCIÓN: INICIO ---
    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        
        st.subheader("📸 Galería de Funciones (Pasarela)")
        tab_img1, tab_img2, tab_img3 = st.tabs(["📊 Planeación", "📝 Evaluación", "🖍️ Materiales"])
        with tab_img1:
            st.image("https://via.placeholder.com/1200x400.png?text=Planeaciones+Alineadas+a+la+NEM", use_container_width=True)
        with tab_img2:
            st.image("https://via.placeholder.com/1200x400.png?text=Generación+de+Rúbricas+y+Exámenes", use_container_width=True)
        with tab_img3:
            st.image("https://via.placeholder.com/1200x400.png?text=Sugerencias+de+Libros+de+Texto+SEP", use_container_width=True)

        st.divider()
        st.subheader("📺 ¿Cómo funciona?")
        col_v1, col_v2 = st.columns([2, 1])
        with col_v1:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Reemplaza con tu video
        with col_v2:
            st.markdown("""
            ### Beneficios Clave:
            * ✅ Ahorra hasta 10 horas semanales.
            * ✅ Alineado a Campos Formativos.
            * ✅ Basado en el Programa Sintético.
            * ✅ Resultados en segundos.
            """)

    # --- SECCIÓN: ACERCA DE ---
    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia y Misión</h1>", unsafe_allow_html=True)
        col_text, col_img = st.columns([1.5, 1])
        with col_text:
            st.markdown("""
            ### ¿Quiénes somos?
            **Maestro Estratega NEM** nació en el corazón de las aulas mexicanas. No somos solo una plataforma tecnológica; somos un equipo de docentes y desarrolladores que entendemos que el tiempo frente al grupo es lo más valioso, pero que la carga administrativa a menudo nos lo roba.
            
            ### Nuestra Misión
            Nuestra misión es democratizar el acceso a la **Inteligencia Artificial** de última generación para todos los docentes de México. Queremos que la implementación de la **Nueva Escuela Mexicana (NEM)** no sea una carga burocrática, sino una oportunidad para innovar.
            
            ### ¿Por qué confiar en nosotros?
            * **Hecho por maestros:** Entendemos los PDA y Ejes Articuladores.
            * **Tecnología Groq:** La IA más rápida del mercado.
            * **Compromiso Social:** Herramientas accesibles para el magisterio.
            """)
        with col_img:
            st.image("https://images.unsplash.com/photo-1544531585-9847b68c8c86?auto=format&fit=crop&w=500", caption="Transformando la educación")
        st.info("💡 **Dato curioso:** Con nosotros, recuperas hasta 8 horas a la semana de tu tiempo personal.")

    # --- SECCIÓN: CONTACTO ---
    elif choice == "Contacto":
        st.title("📧 Contacto y Soporte")
        st.write("Dudas, aclaraciones o envío de comprobantes de pago.")
        with st.form("contacto"):
            nombre = st.text_input("Nombre completo")
            correo = st.text_input("Correo electrónico")
            mensaje = st.text_area("¿En qué podemos ayudarte?")
            if st.form_submit_button("Enviar Mensaje"):
                st.success(f"Gracias {nombre}, hemos recibido tu mensaje.")

    # --- SECCIÓN: REGISTRO ---
    elif choice == "Registrarse":
        st.subheader("📝 Registro de Nuevo Usuario")
        if st.session_state.get('registro_exitoso'):
            st.markdown("<div class='welcome-card'><h3>🎉 ¡Registro exitoso!</h3><p>Cuenta creada. Por favor <b>Inicia Sesión</b> para activar tu suscripción.</p></div>", unsafe_allow_html=True)
        with st.form("reg"):
            email_reg = st.text_input("Email")
            pw_reg = st.text_input("Contraseña (mín. 6 caracteres)", type="password")
            if st.form_submit_button("Crear Cuenta"):
                if len(pw_reg) >= 6:
                    registrar_usuario(email_reg, pw_reg)
                    st.rerun()
                else: st.error("Contraseña muy corta.")

    # --- SECCIÓN: LOGIN ---
    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso para Maestros")
        with st.form("login"):
            email_log = st.text_input("Email")
            pw_log = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(email_log)
                if u and u['password'] == pw_log:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Email o contraseña incorrectos.")

# --- 6. PANEL DE TRABAJO (USUARIO LOGUEADO) ---
else:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.write(f"Maestro: **{st.session_state.user['email']}**")
        st.write(f"Estatus: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    # BLOQUEO SI EL PLAN ES GRATIS
    if st.session_state.user['plan'] == "Gratis":
        st.warning("🚨 Tu suscripción no está activa.")
        st.title("💎 Elige tu método de activación")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("<div class='price-card-selected'><h3>PLAN ANUAL</h3><h1>$899</h1><small>MXN / Año</small></div>", unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("Pagar con Tarjeta (Stripe)", "https://buy.stripe.com/LINK_ANUAL", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>Transferencia / OXXO:</strong><br>Banco: BBVA<br>CLABE: 0123 4567 8901 2345 67<br>Beneficiario: Tu Nombre</div>", unsafe_allow_html=True)
        
        with col_p2:
            st.markdown("<div class='price-card-selected'><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1><small>MXN / Total</small></div>", unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("Pagar con PayPal", "https://paypal.me/usuario", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>Depósito Bancario:</strong><br>Monto: $1,999.00<br>Concepto: Licencia 3 Años</div>", unsafe_allow_html=True)
        
        st.info("Una vez pagado, envía tu ticket en la sección de 'Contacto' para activar tu acceso.")
    
    # ACCESO A LA IA (SÓLO SI EL PLAN NO ES GRATIS)
    else:
        st.title("🤖 Estación de Planeación Inteligente")
        tema = st.text_input("Escribe el tema o PDA:")
        if st.button("Generar Planeación"):
            with st.spinner("Construyendo..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Eres experto en NEM. Genera planeación sobre: {tema}"}]
                    )
                    st.markdown(completion.choices[0].message.content)
                except Exception as e: st.error("Error en conexión con la IA.")

# --- 7. PIE DE PÁGINA (COPYRIGHT) ---
st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Todos los derechos reservados | Matamoros, Tam.</p></div>", unsafe_allow_html=True)