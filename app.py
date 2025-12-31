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
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Error de configuración de Base de Datos.")

# --- INICIALIZACIÓN DE HISTORIAL (NUEVO) ---
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
    <head><style>table {{ border-collapse: collapse; width: 100%; font-family: sans-serif; }} th, td {{ border: 1px solid black; padding: 8px; text-align: left; }} th {{ background-color: #f2f2f2; }}</style></head>
    <body style='padding: 20px;'>
    <h1 style='text-align: center; color: #1e3a8a;'>{nombre_proyecto}</h1>
    <div>{contenido}</div>
    </body></html>
    """
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{nombre_proyecto}.html" style="text-decoration:none;"><button style="width:100%; cursor:pointer; background-color:#1e3a8a; color:white; padding:10px; border:none; border-radius:10px; font-weight:bold;">📄 Descargar Formato Impresión (PDF)</button></a>'

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

# --- 5. ESTILOS CSS (MANTENIDOS) ---
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 40px; background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; border-radius: 15px; margin-bottom: 20px; }
    .price-card { border: 1px solid #e2e8f0; padding: 25px; border-radius: 15px; text-align: center; background-color: #ffffff; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .payment-box { background-color: #f1f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVEGACIÓN ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>IA diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        st.markdown("### Beneficios\n* **✅ Ahorro Real**\n* **✅ Alineación Total**\n* **✅ Libros de Texto SEP 2024 Vigentes**")

    elif choice == "Acerca de":
        st.markdown("### Nuestra Historia y Misión\nMaestro Estratega NEM nació en el corazón de las aulas mexicanas...")

    elif choice == "Registrarse":
        with st.form("reg"):
            email = st.text_input("Correo electrónico"); pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Siguiente"):
                st.session_state.temp_email, st.session_state.temp_pw, st.session_state.show_options = email, pw, True
        if st.session_state.get('show_options'):
            c1, c2, c3 = st.columns(3)
            with c1: 
                if st.button("🎁 Cortesía"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Cortesía"); st.rerun()
            with c2:
                if st.button("📅 Plan Anual"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"); st.rerun()
            with c3:
                if st.button("💎 Plan 3 Años"): registrar_usuario(st.session_state.temp_email, st.session_state.temp_pw, "Pendiente"); st.rerun()

    elif choice == "Iniciar Sesión":
        with st.form("login"):
            e = st.text_input("Email"); p = st.text_input("Password", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(e)
                if u and u['password'] == p: st.session_state.user = u; st.rerun()

else:
    # --- PANEL LOGUEADO ---
    plan_user = st.session_state.user['plan']
    if plan_user == "Pendiente":
        st.title("💎 Activa tu Licencia Profesional")
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("<div class='price-card'><h3>PLAN ANUAL</h3><h1>$899</h1></div>", unsafe_allow_html=True)
            st.link_button("🔥 Pagar con Stripe", "https://buy.stripe.com/TU_LINK")
            st.markdown("<div class='payment-box'>CLABE BBVA: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)
        with c_p2:
            st.markdown("<div class='price-card'><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1></div>", unsafe_allow_html=True)
            st.link_button("🔵 Pagar con PayPal", "https://paypal.me/USUARIO")

    else:
        st.title("🤖 Estación de Planeación Inteligente")
        
        # --- SECCIÓN DE HISTORIAL (NUEVO) ---
        if st.session_state.historial_planeaciones:
            with st.expander("📂 Ver planeaciones generadas anteriormente en esta sesión"):
                for idx, plan in enumerate(reversed(st.session_state.historial_planeaciones)):
                    st.write(f"**{idx+1}. {plan['nombre']}** - {plan['fecha']}")
                    if st.button(f"Recuperar: {plan['nombre']}", key=f"btn_hist_{idx}"):
                        st.session_state.resultado = plan['contenido']
                        st.session_state.nombre_p = plan['nombre']
                        st.rerun()
                st.divider()

        with st.form("planeacion_nem"):
            col1, col2, col3 = st.columns(3)
            with col1:
                fase = st.selectbox("Fase", ["Fase 3", "Fase 4", "Fase 5", "Fase 6"])
                grado = st.selectbox("Grado", ["1°", "2°", "3°", "4°", "5°", "6°"])
                seccion = st.text_input("Sección", value="A")
            with col2:
                campo = st.selectbox("Campo Formativo", ["Lenguajes", "Saberes y P. Científico", "Ética, Nat. y Soc.", "De lo Humano y lo Com."])
                escenario = st.selectbox("Escenario", ["Aula", "Escolar", "Comunitario"])
            with col3:
                duracion = st.select_slider("Temporalidad", options=["1 día", "3 días", "1 semana", "2 semanas", "1 mes"])
                ejes = st.multiselect("Ejes", ["Inclusión", "Pensamiento Crítico", "Vida Saludable", "Artes"])
            
            tema = st.text_area("Tema o problemática:")
            
            if st.form_submit_button("✨ GENERAR PLANEACIÓN"):
                if tema:
                    with st.spinner("Vinculando con Programa Sintético y Libros SEP 2024..."):
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        prompt = f"""
                        Eres experto NEM 2024 de la SEP. Genera planeación para {grado} de {fase}, Sección {seccion}.
                        Campo: {campo}, Escenario: {escenario}. DURACIÓN EXACTA: {duracion}.
                        Tema: {tema}.
                        
                        REQUISITOS DE FORMATO:
                        1. TODO EL RESULTADO DEBE ESTAR EN TABLAS DE MARKDOWN.
                        2. TABLA 1: Datos generales, Contenido oficial y PDA (Programa Sintético vigente).
                        3. TABLA 2: Vinculación con Libros de Texto Gratuitos (LTG) 2024: Nombre del Proyecto y PÁGINAS EXACTAS.
                        4. TABLA 3: Secuencia Didáctica por sesión (45-50 min):
                           - INICIO (10 min): Actividad y Materiales específicos.
                           - DESARROLLO (30 min): Actividad central y Materiales específicos.
                           - CIERRE (10 min): Metacognición y Evaluación.
                        
                        Asegúrate de que el número de sesiones coincida con la temporalidad de {duracion}.
                        """
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                        
                        # Guardar resultado y añadir al historial
                        nuevo_nombre = f"Proyecto: {tema[:30]}"
                        nuevo_contenido = res.choices[0].message.content
                        
                        st.session_state.resultado = nuevo_contenido
                        st.session_state.nombre_p = nuevo_nombre
                        
                        st.session_state.historial_planeaciones.append({
                            "nombre": nuevo_nombre,
                            "contenido": nuevo_contenido,
                            "fecha": datetime.now().strftime("%H:%M:%S")
                        })
                        st.rerun()

        if 'resultado' in st.session_state:
            st.divider()
            st.subheader(f"📍 {st.session_state.nombre_p}")
            st.markdown(st.session_state.resultado)
            
            c_d1, c_d2 = st.columns(2)
            word_data = crear_word(st.session_state.resultado, st.session_state.nombre_p)
            c_d1.download_button("📄 Descargar en Word", word_data, f"{st.session_state.nombre_p}.docx", use_container_width=True)
            c_d2.markdown(generar_pdf_html(st.session_state.resultado, st.session_state.nombre_p), unsafe_allow_html=True)

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM</p></div>", unsafe_allow_html=True)

