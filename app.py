import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime
from docx import Document  # Librería para el Word
from docx.shared import Pt
import io

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de conexión con la base de datos.")

# --- 3. FUNCIONES DE EXPORTACIÓN (CORREGIDA PARA FUNCIONAR BIEN) ---
def crear_word(contenido, titulo_doc):
    doc = Document()
    doc.add_heading(titulo_doc, 0)
    # Dividimos el contenido para que el Word respete los párrafos
    for linea in contenido.split('\n'):
        p = doc.add_paragraph(linea)
        p.style.font.size = Pt(11)
    
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- 4. FUNCIONES DE LÓGICA ---
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
    except:
        return False

def obtener_usuario(email):
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except:
        return None

# --- 5. ESTILOS CSS (MANTENIENDO TU DISEÑO LLAMATIVO INTACTO) ---
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

# --- 6. NAVEGACIÓN (USUARIO NO LOGUEADO) ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🚀 Galería de Funciones", "📺 Video Tutorial", "📋 Beneficios"])
        with t1:
            st.image("https://via.placeholder.com/1200x400?text=Planeaciones+Automáticas+NEM")
        with t2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        with t3:
            st.markdown("### ¿Por qué elegirnos?\n* **✅ Ahorro Real:** Hasta 10 horas libres por semana.\n* **✅ Alineación Total:** Con el Programa Sintético 2024.\n* **✅ Hecho por Maestros:** Entendemos tu labor diaria.")

    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia</h1>", unsafe_allow_html=True)
        st.write("Maestro Estratega NEM nació en el corazón de las aulas mexicanas...")

    elif choice == "Registrarse":
        st.subheader("📝 Registro")
        with st.form("reg"):
            email = st.text_input("Email"); pw = st.text_input("Password", type="password")
            if st.form_submit_button("Continuar"):
                st.session_state.temp_email, st.session_state.temp_pw, st.session_state.show_options = email, pw, True
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

# --- 7. PANEL DE CONTROL (LOGUEADO) ---
else:
    with st.sidebar:
        st.write(f"Estatus: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"): del st.session_state.user; st.rerun()

    plan_user = st.session_state.user['plan']

    if plan_user == "Pendiente":
        st.title("💎 Activa tu Licencia Profesional")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("<div class='price-card'><span class='price-tag'>RECOMENDADO</span><h3>PLAN ANUAL</h3><h1>$899</h1></div>", unsafe_allow_html=True)
            st.link_button("🔥 Pagar con Stripe", "https://buy.stripe.com/TU_LINK")
            st.markdown("<div class='payment-box'><strong>Depósito/OXXO:</strong><br>BBVA CLABE: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)
        with col_p2:
            st.markdown("<div class='price-card'><span class='price-tag'>AHORRO</span><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1></div>", unsafe_allow_html=True)
            st.link_button("🔵 PayPal", "https://paypal.me/USUARIO")
            st.markdown("<div class='payment-box'><strong>Transferencia:</strong><br>CLABE: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)

    else:
        # --- 8. GENERADOR PROFESIONAL ---
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
            
            tema = st.text_area("Tema o problemática del proyecto:")
            
            if st.form_submit_button("🚀 GENERAR PLANEACIÓN INTEGRAL"):
                if tema:
                    with st.spinner("Vinculando con Programa Sintético y Libros de Texto..."):
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        prompt = f"""
                        Genera una planeación NEM para {fase}, Campo {campo}, Escenario {escenario} por {duracion}.
                        Tema: {tema}.
                        REQUISITOS:
                        1. TABLA inicial con Contenido oficial y PDA (extraídos del Programa Sintético).
                        2. VINCULACIÓN: Nombre del Proyecto y PÁGINAS EXACTAS en Libros de Texto Gratuitos.
                        3. SECUENCIA (Sesiones de 45-50 min):
                           - INICIO (10 min): Actividad y tiempo.
                           - DESARROLLO (25-30 min): Actividad y tiempo.
                           - CIERRE (10 min): Actividad y tiempo.
                        Presenta todo en tablas y títulos organizados.
                        """
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                        st.session_state.resultado = res.choices[0].message.content
                        st.markdown(st.session_state.resultado)

        if 'resultado' in st.session_state:
            st.divider()
            col_d1, col_d2 = st.columns(2)
            word_file = crear_word(st.session_state.resultado, "Planeación Maestro Estratega NEM")
            col_d1.download_button("📄 Descargar en Word", word_file, "Planeacion_NEM.docx")
            col_d2.info("Para PDF: Presiona Ctrl+P y 'Guardar como PDF' en tu navegador.")

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM</p></div>", unsafe_allow_html=True)
