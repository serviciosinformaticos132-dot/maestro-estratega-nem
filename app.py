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
    st.error("Error de configuración de Base de Datos.")

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

# --- 4. ESTILOS CSS MEJORADOS (MÁS LLAMATIVOS) ---
st.markdown("""
    <style>
    /* Globales */
    .main { background-color: #f8faff; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    
    /* Hero Section */
    .hero-text { text-align: center; padding: 50px; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; border-radius: 20px; margin-bottom: 30px; shadow: 0 10px 20px rgba(0,0,0,0.1); }
    
    /* Tarjetas de Planes de Pago */
    .price-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }
    .price-card:hover { transform: translateY(-5px); border-color: #3b82f6; }
    .price-card h3 { color: #1e3a8a; font-size: 24px; margin-bottom: 10px; }
    .price-card h1 { color: #3b82f6; font-size: 48px; margin-bottom: 5px; }
    .price-tag { background: #eff6ff; color: #1e40af; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 14px; }
    
    /* Cuadros de información bancaria */
    .payment-box {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 1px dashed #3b82f6;
        margin-top: 15px;
        text-align: left;
        font-size: 14px;
        color: #334155;
    }
    
    /* Submenú Flotante de Registro */
    .floating-menu {
        background: white;
        padding: 40px;
        border-radius: 25px;
        border: 2px solid #3b82f6;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        margin-top: 25px;
    }
    
    /* Botones Estilizados */
    div.stButton > button {
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
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
            """)
        with col_img:
            st.image("https://images.unsplash.com/photo-1544531585-9847b68c8c86?auto=format&fit=crop&w=500")

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
                else: st.error("Por favor completa los campos correctamente.")

        if st.session_state.get('show_options'):
            st.markdown("<div class='floating-menu'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>🎯 ¡Casi listo! Selecciona tu plan:</h3>", unsafe_allow_html=True)
            c_opt1, c_opt2, c_opt3 = st.columns(3)
            with c_opt1:
                if st.button("🎁 Acceso de Cortesía", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Cortesía"):
                        st.success("¡Acceso activado! Inicia Sesión.")
            with c_opt2:
                if st.button("📅 Plan Anual ($899)", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"):
                        st.info("Cuenta creada. Activa al iniciar sesión.")
            with c_opt3:
                if st.button("💎 Plan 3 Años ($1,999)", use_container_width=True):
                    if registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"):
                        st.info("Cuenta creada. Activa al iniciar sesión.")
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
        st.markdown("<h2 style='text-align: center;'>💎 Activa tu Licencia Profesional</h2>", unsafe_allow_html=True)
        st.warning("Tu cuenta está registrada. Selecciona uno de los siguientes planes para desbloquear todas las herramientas.")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("""
                <div class='price-card'>
                    <span class='price-tag'>RECOMENDADO</span>
                    <h3>PLAN ANUAL</h3>
                    <h1>$899</h1>
                    <p>Acceso total por 12 meses</p>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("🔥 Pagar con Tarjeta (Stripe)", "https://buy.stripe.com/TU_LINK", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>Depósito OXXO / BBVA:</strong><br>Banco: BBVA<br>CLABE: 0123 4567 8901 2345 67<br>Beneficiario: Tu Nombre</div>", unsafe_allow_html=True)
        
        with col_p2:
            st.markdown("""
                <div class='price-card'>
                    <span class='price-tag'>AHORRO MÁXIMO</span>
                    <h3>PLAN 3 AÑOS</h3>
                    <h1>$1,999</h1>
                    <p>La mejor inversión a largo plazo</p>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("🔵 Pagar con PayPal", "https://paypal.me/USUARIO", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>Transferencia SPEI:</strong><br>CLABE: 0123 4567 8901 2345 67<br>Concepto: Licencia 3 Años</div>", unsafe_allow_html=True)
        st.info("💡 Una vez realizado el pago, envía tu comprobante en la sección de 'Contacto' para activar tu cuenta de inmediato.")

    else:
        # --- FORMULARIO DE PLANEACIÓN COMPLETO ---
        st.title("🤖 Estación de Planeación Inteligente")
        with st.form("planeacion"):
            c1, c2 = st.columns(2)
            with c1:
                grado = st.selectbox("Grado Escolar", ["1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", "5° Primaria", "6° Primaria", "Secundaria"])
                campo = st.selectbox("Campo Formativo", ["Lenguajes", "Saberes", "Ética", "Humanitario"])
            with c2:
                metodologia = st.selectbox("Metodología", ["Proyectos", "STEAM", "ABP", "AS"])
                ejes = st.multiselect("Ejes Articuladores", ["Inclusión", "Pensamiento Crítico", "Vida Saludable"])
            
            pda = st.text_area("PDA / Contenido:", height=100)
            if st.form_submit_button("✨ GENERAR PLANEACIÓN"):
                if pda:
                    with st.spinner("IA Generando..."):
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Planeación NEM: {pda}"}])
                        st.markdown(res.choices[0].message.content)

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Soporte: contacto@tuapp.com</p></div>", unsafe_allow_html=True)
