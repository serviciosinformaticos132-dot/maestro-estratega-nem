import streamlit as st
from groq import Groq

# Configuración de página
st.set_page_config(page_title="Maestro Estratega NEM (Gratis)", page_icon="🇲🇽", layout="wide")

# Logo y Título
try:
    st.image("logo.png", width=150)
except:
    st.write("Logo no encontrado")

# Barra lateral
with st.sidebar:
    # Intentamos jalar la llave de Secrets, si no, la pedimos
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("Conectado al motor gratuito.")
    else:
        api_key = st.text_input("Ingresa tu Groq API Key (gsk_...)", type="password")
    
    st.divider()
    num_preguntas = st.slider("Reactivos para el examen", 5, 20, 10)

# Entradas del Maestro
col1, col2 = st.columns(2)
with col1:
    nivel_edu = st.selectbox("Nivel", ["Preescolar", "Primaria", "Secundaria"])
    grado_edu = st.text_input("Grado", placeholder="Ej: 5º A")
    metodologia = st.selectbox("Metodología", ["Proyectos Comunitarios", "STEAM", "ABP", "Aprendizaje Servicio"])

with col2:
    tema_problema = st.text_area("Tema o Problemática:")
    materiales_tengo = st.text_input("Materiales que ya tienes (opcional):")

# El Súper Prompt para la NEM
SISTEMA_PROMPT = f"""
Eres un experto en la Nueva Escuela Mexicana. Genera:
1. Planeación (Campos Formativos, Ejes articuladores, Contenidos y PDA de acuerdo a cada campo formativo, Perfil de egreso, todo enfocado a la NEM).
2. Secuencia Didáctica (Inicio, Desarrollo, Cierre, las clases son de 50 minutos como máximo).
3. Materiales: Físicos y Digitales (ajustados a: {materiales_tengo}).
4. Sugerencia de Libros SEP.
5. Examen de {num_preguntas} preguntas con clave.
6. Rúbrica Formativa.
Usa un tono profesional y cita los programas sintéticos 2022.
"""

if st.button("🚀 GENERAR PROYECTO GRATUITO"):
    if not api_key:
        st.error("Por favor, ingresa tu API Key de Groq.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner("La IA está trabajando gratis para ti..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SISTEMA_PROMPT},
                        {"role": "user", "content": f"Proyecto para {nivel_edu} {grado_edu}. Tema: {tema_problema}."}
                    ],
                    model= "llama-3.3-70b-versatile", # El mejor modelo gratuito de Groq
                )
                
                respuesta = chat_completion.choices[0].message.content
                st.markdown("---")
                st.markdown(respuesta)
                
                st.download_button("📩 Descargar Planeación", respuesta, file_name="Planeacion_NEM.txt")
        except Exception as e:

            st.error(f"Error: {e}")









