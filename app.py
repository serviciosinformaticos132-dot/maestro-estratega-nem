import streamlit as st
from groq import Groq
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero) ---
st.set_page_config(page_title="Maestro Estratega NEM Pro", page_icon="🇲🇽", layout="wide")

# --- 2. INICIALIZAR FIREBASE ---
if not firebase_admin._apps:
    try:
        # En Streamlit Cloud, asegúrate de que el JSON de Firebase esté pegado tal cual en Secrets
        fb_dict = dict(st.secrets["firebase"])
        creds = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(creds)
    except Exception as e:
        st.error(f"Error conectando a Firebase: {e}")

db = firestore.client()

# --- 3. FUNCIONES DE USUARIO ---
def registrar_usuario(email, password):
    user_ref = db.collection("usuarios").document(email)
    if not user_ref.get().exists:
        user_ref.set({
            "password": password,
            "fecha_registro": datetime.now(),
            "plan": "Trial"
        })
        return True
    return False

def verificar_login(email, password):
    user_ref = db.collection("usuarios").document(email).get()
    if user_ref.exists:
        data = user_ref.to_dict()
        if data["password"] == password:
            return data
    return None

# --- 4. LÓGICA DE ACCESO (LOGIN/REGISTRO) ---
if 'user' not in st.session_state:
    st.image("https://raw.githubusercontent.com/ArielSalgado/logo/main/logo_nem_estratega.png", width=150)
    st.title("🤖 Maestro Estratega NEM Pro")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        with st.form("login_form"):
            email_log = st.text_input("Correo electrónico")
            pass_log = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("Entrar")
            if btn_login:
                user_data = verificar_login(email_log, pass_log)
                if user_data:
                    st.session_state.user = user_data
                    st.session_state.email = email_log
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")

    with tab2:
        with st.form("reg_form"):
            email_reg = st.text_input("Nuevo Correo")
            pass_reg = st.text_input("Nueva Contraseña", type="password")
            btn_reg = st.form_submit_button("Crear cuenta gratuita (7 días)")
            if btn_reg:
                if registrar_usuario(email_reg, pass_reg):
                    st.success("¡Cuenta creada con éxito! Ahora puedes iniciar sesión.")
                else:
                    st.error("Este correo ya está registrado.")

# --- 5. PANEL PRINCIPAL (CUANDO YA INICIÓ SESIÓN) ---
else:
    # Gestión de días restantes
    fecha_reg = st.session_state.user["fecha_registro"]
    
    # Manejo de fecha (Firebase devuelve objetos Timestamp)
    if hasattr(fecha_reg, 'replace'): # Si ya es datetime
        fecha_dt = fecha_reg.replace(tzinfo=None)
    else: # Si es Timestamp de Firebase
        fecha_dt = datetime.fromtimestamp(fecha_reg.timestamp())

    limite = fecha_dt + timedelta(days=7)
    dias_restantes = (limite - datetime.now()).days

    # Barra lateral de usuario
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/ArielSalgado/logo/main/logo_nem_estratega.png", width=100)
        st.write(f"👤 **{st.session_state.email}**")
        
        if st.session_state.user["plan"] == "Trial":
            st.info(f"⏳ Días de prueba: {max(0, dias_restantes)}")
        
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Verificar si el periodo de prueba expiró
    if dias_restantes < 0 and st.session_state.user["plan"] == "Trial":
        st.warning("⏳ Tu prueba de 7 días ha terminado.")
        st.subheader("💰 Elige un Plan para continuar")
        c1, c2 = st.columns(2)
        c1.link_button("Plan Anual ($899)", "https://buy.stripe.com/tu_link_1")
        c2.link_button("Plan 3 Años ($1,999)", "https://buy.stripe.com/tu_link_2")
    
    else:
        # --- AQUÍ EMPIEZA TU CÓDIGO ORIGINAL DE LA IA ---
        st.title("🤖 Asistente Docente Integral")
        
        # Configuración de Groq
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
        else:
            api_key = st.sidebar.text_input("Ingresa tu Groq API Key", type="password")

        # Entradas del Maestro
        col1, col2 = st.columns(2)
        with col1:
            nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
            grado_edu = st.text_input("Grado", placeholder="Ej: 5º A")
            metodologia = st.selectbox("Metodología", ["Proyectos Comunitarios", "STEAM", "ABP", "Aprendizaje Servicio"])
            num_preguntas = st.slider("Reactivos para el examen", 5, 20, 10)

        with col2:
            tema_problema = st.text_area("Tema o Problemática:")
            materiales_tengo = st.text_input("Materiales que ya tienes (opcional):")

        # Prompt optimizado
        SISTEMA_PROMPT = f"""
        Rol: Actúa como un Asesor Técnico Pedagógico (ATP) experto en la Nueva Escuela Mexicana (NEM).
        Tarea: Generar una planeación didáctica completa utilizando la metodología {metodologia}.
        Grado: {grado_edu} de {nivel_edu}.
        Tema: {tema_problema}.
        Materiales base: {materiales_tengo}.
        Requisitos: Incluir PDA, Ejes articuladores, secuencia didáctica detallada, evaluación formativa y un examen de {num_preguntas} preguntas.
        """

        if st.button("🚀 GENERAR PROYECTO"):
            if not api_key:
                st.error("Falta la API Key de Groq.")
            elif not tema_problema:
                st.error("Por favor describe un tema o problemática.")
            else:
                try:
                    client = Groq(api_key=api_key)
                    with st.spinner("La IA está trabajando para ti..."):
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": SISTEMA_PROMPT},
                                {"role": "user", "content": f"Proyecto para {nivel_edu} {grado_edu}. Tema: {tema_problema}."}
                            ],
                            model="llama-3.1-70b-versatile",
                        )
                        
                        respuesta = chat_completion.choices[0].message.content
                        st.markdown("---")
                        st.markdown(respuesta)
                        st.download_button("📩 Descargar Planeación", respuesta, file_name=f"Planeacion_{grado_edu}.txt")
                except Exception as e:
                    st.error(f"Error en la IA: {e}")