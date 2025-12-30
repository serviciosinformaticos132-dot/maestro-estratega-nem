import streamlit as st
from groq import Groq

# Configuración de página
st.set_page_config(page_title="Maestro Estratega NEM (Gratis)", page_icon="🇲🇽", layout="wide")

# Logo y Título
st.image("https://raw.githubusercontent.com/ArielSalgado/logo/main/logo_nem_estratega.png", width=150)
st.title("🤖 Asistente Docente Integral (Motor Groq)")

# Barra lateral
with st.sidebar:
    st.header("⚙️ Configuración")
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
Actúa como un Especialista en Diseño Curricular de la Nueva Escuela Mexicana (NEM). Tu objetivo es diseñar una Propuesta Pedagógica Integral para el grado [Insertar Grado] de Educación [Primaria/Secundaria], basada estrictamente en el Plan de Estudio 2022 y los Programas Sintéticos vigentes.

CONTEXTO DEL PROYECTO:

Temporalidad: [1 o 2 semanas].

Escenario: [Aula / Escolar / Comunitario].

Libro de Texto de referencia: [Nombre del Libro de Proyectos y nombre del Proyecto específico].

Materiales disponibles: {materiales_tengo}.

REQUERIMIENTOS ESTRUCTURALES:

1. Dosificación Curricular (Basada en Programa Sintético):

Identifica el Campo Formativo rector y su metodología asociada (Aprendizaje Basado en Proyectos Comunitarios para Lenguajes; Indagación STEAM para Saberes; Aprendizaje Basado en Problemas para Ética, Naturaleza y Sociedades; o Aprendizaje Servicio para De lo Humano y lo Comunitario).

Selecciona los Contenidos y Procesos de Desarrollo de Aprendizaje (PDA) que se vinculan de forma interdisciplinaria.

Define los Ejes Articuladores que atraviesan el proyecto y el rasgo del Perfil de Egreso al que impacta.

2. Secuencia Didáctica (Momentos de la Metodología NEM):

Diseña sesiones de 50 minutos. Cada día debe incluir al menos 3 actividades dinámicas (Indagación, producción o reflexión).

La estructura debe seguir las fases/momentos de la metodología sociocrítica elegida (ej. "Lanzamiento, Indagación, Creatividad" o "Presentemos, Recolectemos, Formulemos el problema", etc.).

3. Vinculación con Libros de Texto (LTG):

Indica las páginas específicas del libro de Proyectos, del libro Nuestros Saberes (para sustento teórico) y, si aplica, de Múltiples Lenguajes.

4. Recursos y Materiales:

Lista de materiales físicos y digitales aprovechando {materiales_tengo}.

5. Evaluación Formativa Multidimensional:

Diseña un examen de {num_preguntas} preguntas (situacionales, no memorísticas) con clave de respuestas.

Crea una Rúbrica Analítica con niveles de desempeño (Logrado, En Proceso, Requiere Apoyo).

Propón dos instrumentos adicionales basados en el libro "Las estrategias y los instrumentos de evaluación desde el enfoque formativo" (ej. Diario de clase, Escala de actitudes, Guía de observación o Portafolio de evidencias).

FORMATO DE SALIDA: Organiza la información en tablas para la planeación y la secuencia, usando un tono profesional, empático y pedagógicamente sólido.
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
                    model="llama-3.1-70b-versatile", # El mejor modelo gratuito de Groq
                )
                
                respuesta = chat_completion.choices[0].message.content
                st.markdown("---")
                st.markdown(respuesta)
                
                st.download_button("📩 Descargar Planeación", respuesta, file_name="Planeacion_NEM.txt")
        except Exception as e:
            st.error(f"Error: {e}")