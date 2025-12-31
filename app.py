import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime
from docx import Document
import io

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de conexión. Verifica tus credenciales.")

# --- 3. FUNCIONES DE EXPORTACIÓN ---
def crear_word(contenido, titulo_doc):
    doc = Document()
    doc.add_heading(titulo_doc, 0)
    for line in contenido.split('\n'):
        doc.add_paragraph(line)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. FUNCIONES DE LÓGICA ---
def registrar_usuario(email, password, plan_elegido="Pendiente"):
    try:
        data = {"email": str(email), "password": str(password), "plan": plan_elegido, "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        supabase.table("usuarios").insert(data).execute()
        return True
    except: return False

def obtener_usuario(email):
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except: return None

# --- 5. ESTILOS CSS (DISEÑO LLAMATIVO Y COMPLETO) ---
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 50px; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; border-radius: 20px; margin-bottom: 30px; }
    .price-card { background: white; padding: 30px; border-radius: 20px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .price-tag { background: #eff6ff; color: #1e40af; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 14px; }
    .payment-box { background-color: #f8fafc; padding: 15px; border-radius: 12px; border: 1px dashed #3b82f6; margin-top: 15px; text-align: left; font-size: 14px; }
    .floating-menu { background: white; padding: 40px; border-radius: 25px; border: 2px solid #3b82f6; box-shadow: 0 20px 50px rgba(0,0,0,0.15); margin-top: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVEGACIÓN (NO LOGUEADO) ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])
        st.info("Innovación para la educación mexicana.")

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🚀 Galería de Funciones", "📺 Video Tutorial", "📋 Beneficios"])
        with t1:
            st.image("https://via.placeholder.com/1200x400?text=Planeaciones+Automáticas+NEM", use_container_width=True)
            st.image("https://via.placeholder.com/1200x400?text=Evaluación+y+Rúbricas", use_container_width=True)
        with t2: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        with t3: st.markdown("### ¿Por qué elegirnos?\n* **✅ Ahorro Real:** Recupera hasta 10 horas a la semana.\n* **✅ Alineación Total:** Basado fielmente en los PDA oficiales.\n* **✅ Actualizado:** Incluye referencias a los Libros de Texto 2024.")

    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia y Misión</h1>", unsafe_allow_html=True)
        st.markdown("""
        **Maestro Estratega NEM** nació en el corazón de las aulas mexicanas. Somos un equipo de docentes que entendemos que el tiempo frente al grupo es lo más valioso. 
        Nuestra misión es que la implementación de la **NEM** no sea una carga burocrática, sino una oportunidad para innovar.
        """)

    elif choice == "Contacto":
        st.title("📧 Contacto y Soporte")
        with st.form("contacto"):
            st.text_input("Nombre"); st.text_input("Email"); st.text_area("Mensaje")
            if st.form_submit_button("Enviar"): st.success("Mensaje enviado.")

    elif choice == "Registrarse":
        with st.form("reg_form"):
            email_reg = st.text_input("Email"); pw_reg = st.text_input("Password", type="password")
            if st.form_submit_button("Siguiente"):
                st.session_state.temp_email, st.session_state.temp_pw, st.session_state.show_options = email_reg, pw_reg, True
        if st.session_state.get('show_options'):
            st.markdown("<div class='floating-menu'>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: 
                if st.button("🎁 Cortesía"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Cortesía"); st.rerun()
            with c2:
                if st.button("📅 Plan Anual"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"); st.rerun()
            with c3:
                if st.button("💎 Plan 3 Años"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Iniciar Sesión":
        with st.form("login"):
            e = st.text_input("Email"); p = st.text_input("Password", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(e)
                if u and u['password'] == p: st.session_state.user = u; st.rerun()

else:
    # --- 7. PANEL DE CONTROL (LOGUEADO) ---
    with st.sidebar:
        st.write(f"Maestro: **{st.session_state.user['email']}**")
        if st.button("Cerrar Sesión"): del st.session_state.user; st.rerun()

    plan_user = st.session_state.user['plan']

    if plan_user == "Pendiente":
        st.title("💎 Activa tu Suscripción")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("<div class='price-card'><span class='price-tag'>RECOMENDADO</span><h3>PLAN ANUAL</h3><h1>$899</h1></div>", unsafe_allow_html=True)
            st.link_button("🔥 Pagar con Tarjeta", "https://buy.stripe.com/TU_LINK")
            st.markdown("<div class='payment-box'><strong>Depósito OXXO/BBVA:</strong><br>CLABE: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)
        with col_p2:
            st.markdown("<div class='price-card'><span class='price-tag'>AHORRO</span><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1></div>", unsafe_allow_html=True)
            st.link_button("🔵 PayPal", "https://paypal.me/USUARIO")
            st.markdown("<div class='payment-box'><strong>Transferencia:</strong><br>CLABE: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)

    else:
        # --- 8. GENERADOR DE PLANEACIÓN ---
        st.title("🤖 Estación de Planeación Inteligente")
        with st.form("plan_form"):
            c1, c2 = st.columns(2)
            with c1:
                fase = st.selectbox("Fase/Grado", ["Fase 3: 1°-2°", "Fase 4: 3°-4°", "Fase 5: 5°-6°", "Fase 6: Secundaria"])
                campo = st.selectbox("Campo Formativo", ["Lenguajes", "Saberes", "Ética", "Humanitario"])
                escenario = st.selectbox("Escenario", ["Aula", "Escolar", "Comunitario"])
            with c2:
                duracion = st.select_slider("Temporalidad", options=["1 día", "3 días", "1 semana", "2 semanas", "1 mes"])
                ejes = st.multiselect("Ejes Articuladores", ["Inclusión", "Pensamiento Crítico", "Vida Saludable", "Artes"])
            tema = st.text_area("Tema o problemática:")
            
            if st.form_submit_button("🚀 GENERAR PLANEACIÓN INTEGRAL"):
                if tema:
                    with st.spinner("Construyendo tablas y vinculando libros..."):
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        prompt = f"""
                        Actúa como experto NEM. Genera planeación para {fase}, Campo {campo}, Escenario {escenario}, por {duracion}.
                        Tema: {tema}. 
                        ESTRUCTURA:
                        1. TABLA inicial con: Fase, Campo, Contenido oficial y PDA (buscados en el Programa Sintético).
                        2. VINCULACIÓN: Nombre del Proyecto en Libros de Texto y PÁGINAS EXACTAS.
                        3. SECUENCIA (Sesiones de 45-50 min):
                           - INICIO (10 min): Actividad y tiempo.
                           - DESARROLLO (25-30 min): Actividad y tiempo.
                           - CIERRE (10 min): Actividad y tiempo.
                        4. ESCENARIO: Detalles del tipo de escenario {escenario}.
                        Presenta todo con títulos claros y formato profesional de tabla.
                        """
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                        st.session_state.resultado = res.choices[0].message.content
                        st.markdown(st.session_state.resultado)

        if 'resultado' in st.session_state:
            col_d1, col_d2 = st.columns(2)
            word_file = crear_word(st.session_state.resultado, "Planeación Maestro Estratega")
            col_d1.download_button("📄 Descargar Word", word_file, "Planeacion.docx")
            col_d2.info("Para PDF: Presiona Ctrl+P y 'Guardar como PDF' en tu navegador.")

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM</p></div>", unsafe_allow_html=True)



