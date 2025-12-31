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
    st.error("Error de conexión con la base de datos. Verifica tus Secrets.")

# --- 3. FUNCIONES DE LÓGICA ---
def registrar_usuario(email, password, plan_elegido="Pendiente"):
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
    .payment-box { background-color: #f1f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-top: 10px; font-family: sans-serif; }
    .floating-menu { background-color: #f8f9fa; padding: 30px; border-radius: 20px; border: 2px solid #3b82f6; box-shadow: 0px 10px 30px rgba(0,0,0,0.2); margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVEGACIÓN (NO LOGUEADO) ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])
        st.divider()
        st.info("Innovación para la educación mexicana.")

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        st.subheader("📸 Conoce nuestras herramientas")
        t1, t2, t3 = st.tabs(["🚀 Galería de Funciones", "📺 Video Tutorial", "📋 Beneficios"])
        with t1:
            st.image("https://via.placeholder.com/1200x400?text=Planeaciones+Automáticas+NEM", use_container_width=True)
            st.image("https://via.placeholder.com/1200x400?text=Evaluación+y+Rúbricas", use_container_width=True)
        with t2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        with t3:
            st.markdown("""
            ### ¿Por qué elegirnos?
            * **✅ Ahorro Real:** Recupera hasta 10 horas a la semana de tu tiempo personal.
            * **✅ Alineación Total:** Basado fielmente en los Campos Formativos y Ejes Articuladores.
            * **✅ Actualizado:** Incluye referencias a los Libros de Texto y el Programa Sintético.
            * **✅ Instantáneo:** Genera propuestas pedagógicas en menos de 10 segundos.
            """)

    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia y Misión</h1>", unsafe_allow_html=True)
        col_text, col_img = st.columns([1.5, 1])
        with col_text:
            st.markdown("""
            ### ¿Quiénes somos?
            **Maestro Estratega NEM** nació en el corazón de las aulas mexicanas. No somos solo una plataforma tecnológica; somos un equipo de docentes y desarrolladores que entendemos que el tiempo frente al grupo es lo más valioso.
            
            ### Nuestra Misión
            Nuestra misión es democratizar el acceso a la **Inteligencia Artificial** de última generación para todos los docentes de México. Queremos que la implementación de la **Nueva Escuela Mexicana (NEM)** no sea una carga burocrática, sino una oportunidad para innovar.
            
            ### ¿Por qué confiar en nosotros?
            * **Hecho por maestros:** Entendemos los PDA y Ejes Articuladores.
            * **Tecnología de Vanguardia:** El motor de IA más rápido del mundo.
            * **Compromiso Social:** Herramientas accesibles para el magisterio.
            """)
        with col_img:
            st.image("https://images.unsplash.com/photo-1544531585-9847b68c8c86?auto=format&fit=crop&w=500", caption="Transformando la educación")

    elif choice == "Contacto":
        st.title("📧 Contacto y Soporte")
        with st.form("contacto"):
            st.text_input("Nombre completo"); st.text_input("Correo electrónico"); st.text_area("¿Cómo podemos ayudarte?")
            if st.form_submit_button("Enviar Mensaje"): st.success("Mensaje recibido.")

    elif choice == "Registrarse":
        st.subheader("📝 Registro de Nuevo Maestro")
        with st.form("reg_form"):
            email_reg = st.text_input("Correo electrónico")
            pw_reg = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Continuar a Selección de Plan"):
                if email_reg and len(pw_reg) >= 6:
                    st.session_state['temp_email'] = email_reg
                    st.session_state['temp_pw'] = pw_reg
                    st.session_state['show_options'] = True
                else: st.error("Completa los campos correctamente.")

        if st.session_state.get('show_options'):
            st.markdown("<div class='floating-menu'>", unsafe_allow_html=True)
            st.markdown("### 🎯 Paso Final: Selecciona tu modalidad de acceso")
            c_opt1, c_opt2, c_opt3 = st.columns(3)
            with c_opt1:
                if st.button("🎁 Acceso de Cortesía", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Cortesía"):
                        st.success("¡Acceso de Cortesía activado! Ve a Iniciar Sesión.")
            with c_opt2:
                if st.button("📅 Plan Anual ($899 MXN)", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"):
                        st.info("Cuenta creada. Podrás activar tu acceso al iniciar sesión.")
            with c_opt3:
                if st.button("💎 Plan 3 Años ($1,999 MXN)", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"):
                        st.info("Cuenta creada. Podrás activar tu acceso al iniciar sesión.")
            st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso al Panel")
        with st.form("login"):
            e_log = st.text_input("Correo"); p_log = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(e_log)
                if u and u['password'] == p_log:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Email o contraseña incorrectos.")

# --- 6. PANEL DE CONTROL (LOGUEADO) ---
else:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.write(f"Estatus: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    plan_user = st.session_state.user['plan']

    if plan_user == "Pendiente":
        st.warning("🚨 Tu cuenta requiere activación de licencia.")
        st.title("💎 Elige tu método de activación")
        cp1, cp2 = st.columns(2)
        with cp1:
            st.markdown("<div class='price-card-selected'><h3>PLAN ANUAL</h3><h1>$899</h1></div>", unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("Pago con Tarjeta", "https://buy.stripe.com/LINK1", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>Banco:</strong> BBVA<br><strong>CLABE:</strong> 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)
        with cp2:
            st.markdown("<div class='price-card-selected'><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1></div>", unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("PayPal", "https://paypal.me/usuario", use_container_width=True)
        st.info("💡 Envía tu ticket por 'Contacto' para activar tu acceso.")

    elif plan_user == "Cortesía":
        st.title("🎁 Modo de Cortesía Activo")
        tema = st.text_input("Tema de prueba:")
        if st.button("Generar Propuesta"):
            with st.spinner("Procesando..."):
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":f"Resumen NEM: {tema}"}])
                st.markdown(res.choices[0].message.content)

    else: # Planes pagados
        st.title("🤖 Estación de Planeación Inteligente")
        tema = st.text_input("Escribe el tema o PDA completo:")
        if st.button("Generar Planeación Detallada"):
            with st.spinner("Construyendo planeación..."):
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Planeación detallada NEM: {tema}"}])
                st.markdown(res.choices[0].message.content)

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Soporte: contacto@tuapp.com</p></div>", unsafe_allow_html=True)