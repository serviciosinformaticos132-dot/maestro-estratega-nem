import streamlit as st
from groq import Groq
from supabase import create_client, Client
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Maestro Estratega NEM", page_icon="🇲🇽", layout="wide")

# --- 2. CONEXIÓN A BASE DE DATOS (SUPABASE) ---
# Recuerda configurar estos en Settings > Secrets de Streamlit Cloud
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- 3. FUNCIONES DE LÓGICA DE USUARIOS ---
def registrar_usuario(email, password):
    data = {
        "email": email, 
        "password": password, 
        "plan": "Gratis", 
        "fecha_registro": str(datetime.now())
    }
    supabase.table("usuarios").insert(data).execute()

def obtener_usuario(email):
    res = supabase.table("usuarios").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None

# --- 4. ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #ddd;
        font-size: 14px;
        z-index: 100;
    }
    .hero-text {
        text-align: center;
        padding: 40px;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE NAVEGACIÓN ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])
        st.divider()
        st.info("Innovación para la educación mexicana.")

    # --- SECCIÓN: INICIO ---
    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        st.subheader("📸 Conoce nuestras herramientas")
        t1, t2 = st.tabs(["🚀 Galería de Funciones", "📺 Video Tutorial"])
        with t1:
            st.image("https://via.placeholder.com/1000x400?text=Pasarela+de+Imagenes+de+Planeaciones", use_container_width=True)
        with t2:
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # --- SECCIÓN: ACERCA DE (ACTUALIZADO) ---
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
            * **Hecho por y para maestros:** Entendemos los Campos Formativos y Ejes Articuladores.
            * **Tecnología de Vanguardia:** Usamos el motor de IA más rápido del mundo.
            * **Compromiso Social:** Creemos en dotar a los maestros de las mejores herramientas.
            """)
        with col_img:
            st.image("https://images.unsplash.com/photo-1544531585-9847b68c8c86?auto=format&fit=crop&w=500", 
                     caption="Transformando la educación", use_container_width=True)
        st.info("💡 **Dato curioso:** Un docente promedio recupera hasta 8 horas a la semana usando nuestra IA.")

    # --- SECCIÓN: CONTACTO ---
    elif choice == "Contacto":
        st.title("📧 Contacto")
        with st.form("contacto"):
            nombre = st.text_input("Nombre")
            correo = st.text_input("Correo")
            mensaje = st.text_area("¿Cómo podemos ayudarte?")
            if st.form_submit_button("Enviar Mensaje"):
                st.success(f"Gracias {nombre}, mensaje enviado con éxito.")

    # --- SECCIÓN: REGISTRO ---
    elif choice == "Registrarse":
        st.subheader("📝 Registro de Nuevo Maestro")
        with st.form("reg"):
            email = st.text_input("Correo electrónico")
            pw = st.text_input("Contraseña", type="password")
            confirm = st.text_input("Confirmar contraseña", type="password")
            if st.form_submit_button("Crear Cuenta Gratuita"):
                if pw == confirm and len(pw) > 5:
                    registrar_usuario(email, pw)
                    st.success("Cuenta creada. Ahora ve a 'Iniciar Sesión'.")
                else: st.error("Error: Revisa que las contraseñas coincidan y tengan más de 6 caracteres.")

    # --- SECCIÓN: INICIAR SESIÓN ---
    elif choice == "Iniciar Sesión":
        st.subheader("🔑 Acceso al Panel")
        with st.form("login"):
            email = st.text_input("Correo")
            pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                u = obtener_usuario(email)
                if u and u['password'] == pw:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Credenciales incorrectas.")

# --- 6. PANEL DE CONTROL (USUARIO LOGUEADO) ---
else:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.write(f"Maestro: **{st.session_state.user['email']}**")
        st.write(f"Plan actual: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    st.title("🤖 Estación de Planeación Inteligente")
    st.write("Escribe el tema o contenido del programa sintético que deseas desarrollar.")
    
    tema = st.text_input("Tema de la planeación:")
    if st.button("Generar Propuesta con IA"):
        with st.spinner("Construyendo planeación pedagógica..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Actúa como experto en la NEM y genera una planeación sobre: {tema}"}]
                )
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error al conectar con la IA: {e}")

# --- 7. PIE DE PÁGINA (COPYRIGHT) ---
st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Todos los derechos reservados | Matamoros, Tam.</p></div>", unsafe_allow_html=True)