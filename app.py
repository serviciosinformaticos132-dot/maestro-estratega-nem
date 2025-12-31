import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime
from docx import Document
from docx.shared import Pt
import io
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de configuración de Base de Datos. Revisa los Secrets.")

# --- 3. FUNCIONES DE EXPORTACIÓN ---
def crear_word(contenido, titulo_doc):
    doc = Document()
    doc.add_heading(titulo_doc, 0)
    for line in contenido.split('\n'):
        if line.strip():
            p = doc.add_paragraph(line)
            p.style.font.size = Pt(11)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

def generar_pdf_html(contenido):
    html = f"<html><body style='font-family: Arial;'><pre style='white-space: pre-wrap;'>{contenido}</pre></body></html>"
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="Planeacion_NEM.html" style="text-decoration:none;"><button style="width:100%; cursor:pointer; background-color:#1e3a8a; color:white; padding:10px; border:none; border-radius:10px; font-weight:bold;">📄 Descargar Formato Impresión (PDF)</button></a>'

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
    except Exception as e:
        st.error(f"Error al registrar: {e}")
        return False

def obtener_usuario(email):
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except:
        return None

# --- 5. ESTILOS CSS PERSONALIZADOS (DISEÑO LLAMATIVO MANTENIDO) ---
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 40px; background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; border-radius: 15px; margin-bottom: 20px; }
    .price-card { border: 1px solid #e2e8f0; padding: 25px; border-radius: 15px; text-align: center; background-color: #ffffff; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; transition: 0.3s; }
    .price-card:hover { transform: translateY(-5px); border-color: #3b82f6; }
    .price-tag { background: #eff6ff; color: #1e40af; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 12px; }
    .payment-box { background-color: #f1f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-top: 10px; text-align: left; }
    .floating-menu { background-color: #ffffff; padding: 30px; border-radius: 20px; border: 2px solid #3b82f6; box-shadow: 0px 10px 30px rgba(0,0,0,0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVEGACIÓN (NO LOGUEADO) ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🚀 Galería de Funciones", "📺 Video Tutorial", "📋 Beneficios"])
        with t1:
            st.image("https://via.placeholder.com/1200x400?text=Planeaciones+Automáticas+NEM", use_container_width=True)
        with t2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        with t3:
            st.markdown("""
            ### ¿Por qué elegirnos?
            * **✅ Ahorro Real:** Recupera hasta 10 horas a la semana de tu tiempo personal.
            * **✅ Alineación Total:** Basado fielmente en los Campos Formativos y Ejes Articuladores.
            * **✅ Actualizado:** Incluye referencias a los Libros de Texto y el Programa Sintético 2024.
            * **✅ Instantáneo:** Genera propuestas pedagógicas en menos de 10 segundos.
            """)

    elif choice == "Acerca de":
        st.markdown("<h1 style='text-align: center;'>📖 Nuestra Historia y Misión</h1>", unsafe_allow_html=True)
        st.markdown("""
        **Maestro Estratega NEM** nació en el corazón de las aulas mexicanas. No somos solo una plataforma tecnológica; somos un equipo de docentes y desarrolladores que entendemos que el tiempo frente al grupo es lo más valioso, pero que la carga administrativa a menudo nos lo roba.
        
        Nuestra misión es democratizar el acceso a la **Inteligencia Artificial** de última generación para todos los docentes de México. Queremos que la implementación de la **Nueva Escuela Mexicana (NEM)** no sea una carga burocrática, sino una oportunidad para innovar y conectar mejor con nuestros alumnos.
        """)

    elif choice == "Registrarse":
        st.subheader("📝 Registro de Nuevo Maestro")
        with st.form("reg"):
            email = st.text_input("Correo electrónico"); pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Siguiente"):
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
                else: st.error("Acceso denegado.")

# --- 7. PANEL DE CONTROL (LOGUEADO) ---
else:
    with st.sidebar:
        st.write(f"Maestro: **{st.session_state.user['email']}**")
        if st.button("Cerrar Sesión"): del st.session_state.user; st.rerun()

    plan_user = st.session_state.user['plan']

    if plan_user == "Pendiente":
        st.title("💎 Activa tu Licencia Profesional")
        cp1, cp2 = st.columns(2)
        with cp1:
            st.markdown("<div class='price-card'><span class='price-tag'>RECOMENDADO</span><h3>PLAN ANUAL</h3><h1>$899</h1></div>", unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("🔥 Pagar con Stripe", "https://buy.stripe.com/TU_LINK", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>Depósito OXXO/BBVA:</strong><br>CLABE: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)
        with cp2:
            st.markdown("<div class='price-card'><span class='price-tag'>AHORRO MÁXIMO</span><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1></div>", unsafe_allow_html=True)
            with st.expander("💳 OPCIONES DE PAGO"):
                st.link_button("🔵 Pagar con PayPal", "https://paypal.me/USUARIO", use_container_width=True)
                st.markdown("<div class='payment-box'><strong>Transferencia SPEI:</strong><br>CLABE: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)
    else:
        st.title("🤖 Estación de Planeación Inteligente")
        with st.form("planeacion_nem"):
            col1, col2 = st.columns(2)
            with col1:
                fase = st.selectbox("Fase / Grado Escolar", ["Fase 3: 1° y 2° Primaria", "Fase 4: 3° y 4° Primaria", "Fase 5: 5° y 6° Primaria", "Fase 6: Secundaria"])
                campo = st.selectbox("Campo Formativo", ["Lenguajes", "Saberes y Pensamiento Científico", "Ética, Naturaleza y Sociedades", "De lo Humano y lo Comunitario"])
                escenario = st.selectbox("Escenario", ["Aula", "Escolar", "Comunitario"])
            with col2:
                duracion = st.select_slider("Temporalidad / Duración", options=["1 día", "3 días", "1 semana", "2 semanas", "1 mes"])
                ejes = st.multiselect("Ejes Articuladores", ["Inclusión", "Pensamiento Crítico", "Interculturalidad Crítica", "Igualdad de Género", "Vida Saludable", "Artes", "Fomento a la Lectura"])
            
            tema = st.text_area("Tema o problemática a trabajar:")
            
            if st.form_submit_button("✨ GENERAR PLANEACIÓN INTEGRAL"):
                if tema:
                    with st.spinner("Vinculando contenidos y organizando sesiones..."):
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        prompt = f"""
                        Eres un experto en la NEM 2024. Genera una planeación para {fase}, {campo}, Escenario {escenario}.
                        Temporalidad: {duracion}. Tema: {tema}.
                        
                        ESTRUCTURA OBLIGATORIA:
                        1. TABLA TÉCNICA: Fase, Campo, Contenido oficial y PDA oficial (del Programa Sintético).
                        2. VINCULACIÓN LTG: Nombre del Proyecto, Escenario y PÁGINAS EXACTAS de los libros de la SEP.
                        3. SECUENCIA DIDÁCTICA DETALLADA POR SESIÓN (45-50 MINUTOS):
                           Para CADA sesión genera lo siguiente:
                           - INICIO (10 min): Actividad de rescate y motivación.
                           - DESARROLLO (30 min): Actividad central (Metodologías Sociocríticas).
                           - CIERRE (5-10 min): Metacognición.
                           - MATERIALES: Listado específico de recursos necesarios SOLO para esta sesión.
                        
                        IMPORTANTE: No te limites a 4 sesiones si la temporalidad es mayor. Presenta todo en tablas claras.
                        """
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                        st.session_state.resultado = res.choices[0].message.content
                        st.markdown(st.session_state.resultado)

        if 'resultado' in st.session_state:
            st.divider()
            c_d1, c_d2 = st.columns(2)
            word_data = crear_word(st.session_state.resultado, "Planeación Maestro Estratega NEM")
            c_d1.download_button("📄 Descargar en Word", word_data, "Planeacion.docx", use_container_width=True)
            c_d2.markdown(generar_pdf_html(st.session_state.resultado), unsafe_allow_html=True)

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Matamoros, Tam.</p></div>", unsafe_allow_html=True)

