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

# --- 4. ESTILOS CSS (MANTENIENDO TU DISEÑO LLAMATIVO) ---
st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px; border-top: 1px solid #ddd; font-size: 14px; z-index: 100; }
    .hero-text { text-align: center; padding: 50px; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; border-radius: 20px; margin-bottom: 30px; }
    .price-card { background: white; padding: 30px; border-radius: 20px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .price-tag { background: #eff6ff; color: #1e40af; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 14px; }
    .payment-box { background-color: #f8fafc; padding: 15px; border-radius: 12px; border: 1px dashed #3b82f6; margin-top: 15px; text-align: left; font-size: 14px; }
    .floating-menu { background: white; padding: 40px; border-radius: 25px; border: 2px solid #3b82f6; box-shadow: 0 20px 50px rgba(0,0,0,0.15); margin-top: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVEGACIÓN ---
if 'user' not in st.session_state:
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("🧭 Menú Principal")
        choice = st.radio("Navegación", ["Inicio", "Acerca de", "Contacto", "Registrarse", "Iniciar Sesión"])

    if choice == "Inicio":
        st.markdown("<div class='hero-text'><h1>🍎 Maestro Estratega NEM</h1><p>Inteligencia Artificial diseñada para la Nueva Escuela Mexicana</p></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🚀 Galería", "📺 Tutorial", "📋 Beneficios"])
        with t1: st.image("https://via.placeholder.com/1200x400?text=Planeaciones+Inteligentes+NEM")
        with t2: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        with t3: st.markdown("* ✅ Ahorro Real\n* ✅ Alineación Total\n* ✅ Resultados en segundos")

    elif choice == "Acerca de":
        st.markdown("### Nuestra Historia\nMaestro Estratega NEM nació en el corazón de las aulas mexicanas...")

    elif choice == "Registrarse":
        st.subheader("📝 Registro")
        with st.form("reg"):
            email = st.text_input("Email"); pw = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Continuar"):
                st.session_state.temp_email, st.session_state.temp_pw = email, pw
                st.session_state.show_options = True
        
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
    # --- PANEL LOGUEADO ---
    with st.sidebar:
        st.write(f"Plan: **{st.session_state.user['plan']}**")
        if st.button("Cerrar Sesión"): del st.session_state.user; st.rerun()

    plan_user = st.session_state.user['plan']

    if plan_user == "Pendiente":
        st.title("💎 Activa tu Suscripción")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("<div class='price-card'><h3>PLAN ANUAL</h3><h1>$899</h1></div>", unsafe_allow_html=True)
            st.link_button("🔥 Pagar con Tarjeta", "https://buy.stripe.com/TU_LINK")
            st.markdown("<div class='payment-box'>CLABE BBVA: 0123 4567 8901 2345 67</div>", unsafe_allow_html=True)
        with col_p2:
            st.markdown("<div class='price-card'><h3>PLAN 3 AÑOS</h3><h1>$1,999</h1></div>", unsafe_allow_html=True)
            st.link_button("🔵 Pagar con PayPal", "https://paypal.me/USUARIO")

    else:
        # --- FORMULARIO DE PLANEACIÓN AUTOMATIZADO ---
        st.title("🤖 Estación de Planeación Inteligente")
        st.info("Nueva función: Ya no necesitas copiar el PDA. La IA lo buscará por ti según tu tema.")
        
        with st.form("planeacion_automatica"):
            col_a, col_b = st.columns(2)
            with col_a:
                fase = st.selectbox("Fase / Grado", ["Fase 3: 1° y 2° Primaria", "Fase 4: 3° y 4° Primaria", "Fase 5: 5° y 6° Primaria", "Fase 6: Secundaria"])
                campo = st.selectbox("Campo Formativo", ["Lenguajes", "Saberes y Pensamiento Científico", "Ética, Naturaleza y Sociedades", "De lo Humano y lo Comunitario"])
            with col_b:
                mes = st.selectbox("Mes de aplicación", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
                ejes = st.multiselect("Ejes Articuladores", ["Inclusión", "Pensamiento Crítico", "Interculturalidad Crítica", "Igualdad de Género", "Vida Saludable", "Artes y Experiencias Estéticas"])
            
            # CAMBIO SOLICITADO: Solo tema o problemática
            tema_interes = st.text_area("¿Qué tema o problemática quieres trabajar?", 
                                      placeholder="Ejemplo: El cuidado del agua en mi comunidad o La alimentación saludable y las matemáticas.")
            
            submit_btn = st.form_submit_button("🚀 GENERAR PLANEACIÓN INTEGRAL (PROGRAMA SINTÉTICO + LIBROS)")

        if submit_btn:
            if tema_interes:
                with st.spinner("Buscando en el Programa Sintético y vinculando Libros de Texto..."):
                    try:
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        
                        prompt_pedagogico = f"""
                        Actúa como un Asistente Pedagógico experto en la Nueva Escuela Mexicana (NEM). 
                        Tu tarea es realizar una planeación profesional para {fase}, en el Campo Formativo {campo}.
                        
                        EL MAESTRO QUIERE TRABAJAR ESTE TEMA: "{tema_interes}"
                        
                        INSTRUCCIONES OBLIGATORIAS:
                        1. IDENTIFICACIÓN: Busca y redacta el CONTENIDO oficial y el PROCESO DE DESARROLLO DE APRENDIZAJE (PDA) que mejor se ajuste al tema en el Programa Sintético 2024.
                        2. METODOLOGÍA: Selecciona la metodología sociocrítica adecuada (Proyectos Comunitarios, STEAM, ABP o AS) según el Campo Formativo seleccionado.
                        3. VINCULACIÓN CON LIBROS DE TEXTO: Cita específicamente a qué libro (Proyectos de Aula, Escolares o Comunitarios) y si es posible, las secciones relacionadas.
                        4. SUGERENCIAS METODOLÓGICAS: Utiliza el enfoque del libro 'Diseño Creativo' y 'Sugerencias Metodológicas para el desarrollo de proyectos'.
                        
                        ESTRUCTURA DE RESPUESTA:
                        - Nombre del Proyecto: [Crea un nombre creativo]
                        - Justificación: [Relación del tema con el contexto]
                        - Contenido (Programa Sintético): [Escríbelo tal cual aparece en el programa oficial]
                        - PDA (Programa Sintético): [Escríbelo tal cual aparece en el programa oficial]
                        - Ejes Articuladores: {', '.join(ejes)}
                        - Secuencia Didáctica: (Inicio, Desarrollo, Cierre)
                        - Evaluación Formativa: (Instrumento sugerido)
                        - Referencias SEP: [Cita Libros de Texto Gratuitos vinculados]
                        """
                        
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": "Eres un experto en currículo mexicano NEM 2024."}, {"role": "user", "content": prompt_pedagogico}])
                        
                        st.success("¡Planeación vinculada correctamente!")
                        st.markdown(res.choices[0].message.content)
                    except Exception as e:
                        st.error("Error en la conexión con la IA.")
            else:
                st.warning("Por favor, describe un tema para que la IA pueda buscar los contenidos.")

st.markdown("<div class='footer'><p>© 2025 Maestro Estratega NEM | Matamoros, Tam.</p></div>", unsafe_allow_html=True)


