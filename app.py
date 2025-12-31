import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🍎", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except:
    st.error("Error de conexión.")

# --- INICIALIZACIÓN DE HISTORIAL ---
if 'historial_planeaciones' not in st.session_state:
    st.session_state.historial_planeaciones = []

# --- 3. FUNCIONES DE EXPORTACIÓN ---
def crear_word(contenido, nombre_proyecto):
    doc = Document()
    titulo = doc.add_heading(nombre_proyecto, 0)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(contenido)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

def generar_pdf_html(contenido, nombre_proyecto):
    html = f"""
    <html>
    <head><style>
        body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
        th {{ background-color: #1e3a8a; color: white; }}
        h1 {{ color: #1e3a8a; text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; }}
    </style></head>
    <body>
        <h1>{nombre_proyecto}</h1>
        <div>{contenido.replace('|', '').replace('-', '')}</div>
    </body></html>
    """
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{nombre_proyecto}.html" style="text-decoration:none;"><button style="width:100%; cursor:pointer; background: linear-gradient(45deg, #ef4444, #dc2626); color:white; padding:12px; border:none; border-radius:12px; font-weight:bold; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">📄 Descargar PDF (Formato Impresión)</button></a>'

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

# --- 5. ESTILOS CSS (DASHBOARD MODERNO TIPO APP) ---
st.markdown("""
    <style>
    /* Importación de fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

    /* Fondo general */
    .main { background-color: #f8fafc; }

    /* Hero Section Impactante */
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 60px 20px;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .hero-title { font-size: 3rem; font-weight: 800; margin-bottom: 10px; }
    .hero-subtitle { font-size: 1.2rem; opacity: 0.9; }

    /* Cards estilo App */
    .app-card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Estilo de Precios Moderno */
    .price-card-modern {
        background: white;
        padding: 40px 20px;
        border-radius: 24px;
        border: 2px solid #e2e8f0;
        text-align: center;
        transition: all 0.3s ease;
    }
    .price-card-modern:hover { border-color: #3b82f6; transform: translateY(-10px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1); }
    .price-value { font-size: 3.5rem; font-weight: 800; color: #1e293b; margin: 20px 0; }

    /* Botones tipo iOS/Modernos */
    .stButton>button {
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s;
    }

    /* Footer */
    .footer { text-align: center; padding: 40px; color: #64748b; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVEGACIÓN ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🧭 Menú</h2>", unsafe_allow_html=True)
        choice = st.radio("", ["🏠 Inicio", "📖 Acerca de", "📩 Contacto", "📝 Registrarse", "🔑 Iniciar Sesión"], label_visibility="collapsed")
        st.divider()
        st.info("Plataforma verificada por expertos en la NEM.")

    if choice == "🏠 Inicio":
        st.markdown("""
            <div class='hero-container'>
                <div class='hero-title'>Maestro Estratega NEM</div>
                <div class='hero-subtitle'>La herramienta definitiva para la Nueva Escuela Mexicana</div>
            </div>
        """, unsafe_allow_html=True)
        
        # VIDEO PROMOCIONAL REINTEGRADO
        st.markdown("### 📺 Conoce el poder de nuestra IA")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Reemplazar con link real
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='app-card'><h3>🚀 Rapidez</h3><p>Genera semanas de trabajo en segundos.</p></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='app-card'><h3>📚 Libros 2024</h3><p>Vinculación exacta con la SEP.</p></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='app-card'><h3>🎯 Precisión</h3><p>PDA y Contenidos oficiales.</p></div>", unsafe_allow_html=True)

    elif choice == "📖 Acerca de":
        st.markdown("## Nuestra Historia y Misión")
        st.write("Maestro Estratega NEM nació en el corazón de las aulas mexicanas...")

    elif choice == "📝 Registrarse":
        st.markdown("## Únete a la comunidad")
        with st.form("reg"):
            email = st.text_input("Correo electrónico"); pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Continuar"):
                st.session_state.temp_email, st.session_state.temp_pw, st.session_state.show_options = email, pw, True
        
        if st.session_state.get('show_options'):
            st.markdown("### 🎯 Selecciona tu modalidad")
            c1, c2, c3 = st.columns(3)
            with c1: 
                if st.button("🎁 Cortesía"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Cortesía"); st.rerun()
            with c2:
                if st.button("📅 Plan Anual"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"); st.rerun()
            with c3:
                if st.button("💎 Plan 3 Años"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"); st.rerun()

    elif choice == "🔑 Iniciar Sesión":
        with st.form("login"):
            e = st.text_input("Email"); p = st.text_input("Password", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(e)
                if u and u['password'] == p: st.session_state.user = u; st.rerun()

else:
    # --- PANEL LOGUEADO (DASHBOARD APP) ---
    with st.sidebar:
        st.markdown(f"### Bienvenido<br><span style='color:#3b82f6;'>{st.session_state.user['email']}</span>", unsafe_allow_html=True)
        st.write(f"Plan: **{st.session_state.user['plan']}**")
        st.divider()
        if st.button("Cerrar Sesión", use_container_width=True): del st.session_state.user; st.rerun()

    if st.session_state.user['plan'] == "Pendiente":
        st.title("💎 Activa tu Licencia")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='price-card-modern'><h3>PLAN ANUAL</h3><div class='price-value'>$899</div><p>Acceso total por 12 meses</p></div>", unsafe_allow_html=True)
            st.link_button("💳 Pagar con Tarjeta", "https://buy.stripe.com/TU_LINK", use_container_width=True)
        with c2:
            st.markdown("<div class='price-card-modern'><h3>PLAN 3 AÑOS</h3><div class='price-value'>$1,999</div><p>El plan más ahorrador</p></div>", unsafe_allow_html=True)
            st.link_button("🔵 Pagar con PayPal", "https://paypal.me/USUARIO", use_container_width=True)
    else:
        # --- APP DASHBOARD ---
        st.markdown("## 🤖 Estación de Trabajo Inteligente")
        
        # Historial Colapsable
        if st.session_state.historial_planeaciones:
            with st.expander("📂 Historial de Planeaciones (Sesión Actual)"):
                for idx, plan in enumerate(reversed(st.session_state.historial_planeaciones)):
                    col_h1, col_h2 = st.columns([4, 1])
                    col_h1.write(f"**{plan['nombre']}** ({plan['fecha']})")
                    if col_h2.button("Ver", key=f"rec_{idx}"):
                        st.session_state.resultado = plan['contenido']
                        st.session_state.nombre_p = plan['nombre']
                        st.rerun()

        # Formulario Estilo App
        with st.container():
            st.markdown("<div class='app-card'>", unsafe_allow_html=True)
            with st.form("planeacion_app"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    fase = st.selectbox("Fase", ["Fase 3", "Fase 4", "Fase 5", "Fase 6"])
                    grado = st.selectbox("Grado", ["1°", "2°", "3°", "4°", "5°", "6°"])
                    seccion = st.text_input("Sección", value="A")
                with c2:
                    campo = st.selectbox("Campo Formativo", ["Lenguajes", "Saberes y P. Científico", "Ética, Nat. y Soc.", "De lo Humano y lo Com."])
                    escenario = st.selectbox("Escenario", ["Aula", "Escolar", "Comunitario"])
                with c3:
                    duracion = st.select_slider("Temporalidad", options=["1 día", "3 días", "1 semana", "2 semanas", "1 mes"])
                    ejes = st.multiselect("Ejes Articuladores", ["Inclusión", "Pensamiento Crítico", "Vida Saludable", "Artes"])
                
                tema = st.text_area("Nombre del Proyecto o Problemática:")
                
                if st.form_submit_button("🚀 GENERAR PLANEACIÓN INTEGRAL"):
                    if tema:
                        with st.spinner("⏳ Procesando con IA y Libros SEP 2024..."):
                            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                            prompt = f"""
                            Eres experto NEM 2024. Genera planeación para {grado} de {fase}, Sección {seccion}.
                            Campo: {campo}, Escenario: {escenario}. DURACIÓN: {duracion}.
                            Tema: {tema}.
                            
                            RESULTADO EN TABLAS MARKDOWN:
                            1. TABLA 1: Datos generales, Contenido oficial y PDA vigente.
                            2. TABLA 2: Vinculación con LIBROS SEP 2024 vigentes (PÁGINAS EXACTAS).
                            3. TABLA 3: Secuencia (Sesiones 45-50 min):
                               - INICIO (10 min): Actividad y Materiales.
                               - DESARROLLO (30 min): Actividad y Materiales.
                               - CIERRE (10 min): Metacognición.
                            """
                            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                            st.session_state.resultado = res.choices[0].message.content
                            st.session_state.nombre_p = f"Proyecto: {tema[:40]}"
                            st.session_state.historial_planeaciones.append({"nombre": st.session_state.nombre_p, "contenido": st.session_state.resultado, "fecha": datetime.now().strftime("%H:%M")})
                            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if 'resultado' in st.session_state:
            st.markdown(f"<div class='app-card'><h3>📍 {st.session_state.nombre_p}</h3>", unsafe_allow_html=True)
            st.markdown(st.session_state.resultado)
            
            st.divider()
            d1, d2 = st.columns(2)
            with d1:
                word_data = crear_word(st.session_state.resultado, st.session_state.nombre_p)
                st.download_button("📄 Descargar Word (.docx)", word_data, f"{st.session_state.nombre_p}.docx", use_container_width=True)
            with d2:
                st.markdown(generar_pdf_html(st.session_state.resultado, st.session_state.nombre_p), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>© 2025 Maestro Estratega NEM | Innovación Educativa</div>", unsafe_allow_html=True)


