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
Rol: Actúa como un Asesor Técnico Pedagógico (ATP) experto en la Nueva Escuela Mexicana, con dominio profundo de los Programas Sintéticos 2022 y las metodologías sociocríticas.

Tarea: Generar una planeación didáctica completa de [Insertar Duración: 1 o 2 semanas] para el grado [Grado] sobre el proyecto: [Nombre del Proyecto/Tema], ubicado en el escenario de [Aula/Escolar/Comunitario].

Especificaciones Técnicas Obligatorias:

1. Encuadre Curricular:

Campo Formativo Principal: Elige solo uno como eje rector y asigna su metodología correspondiente (Proyectos Comunitarios, STEAM, ABP o AS).

Transversalidad: Selecciona un segundo campo formativo que se favorezca de manera indirecta.

Elementos: Contenidos, PDA (Programa Sintético), Ejes Articuladores y rasgo del Perfil de Egreso.

2. Secuencia Didáctica por Momentos Metodológicos: Estructura la planeación por Fases o Momentos (según la metodología elegida). Cada sesión de 50 minutos debe contener:

Inicio (1-2 actividades): Recuperación de saberes previos o detonadores.

Desarrollo (Mínimo 3 actividades): Construcción, investigación y acción. Deben ser actividades escritas, lúdicas o de campo, bien detalladas y listas para ejecutar.

Cierre (1 actividad): Enfocada en la evaluación formativa o integración de lo aprendido.

3. Materiales Didácticos Expandidos: Como IA, propón una lista exhaustiva de materiales:

Físicos (incluyendo los de {materiales_tengo}).

Digitales (recursos interactivos, videos o simuladores).

Anexos de Actividades Escritas: Diseña textualmente las instrucciones de fichas de trabajo o ejercicios que el docente debe imprimir o dictar.

4. Atención al Rezago Educativo (Plan de Recuperación): Por cada sesión o al final de la planeación, incluye una sección de "Actividades de Refuerzo Personalizado" dirigidas a alumnos con rezago en:

Lectura y escritura (fluidez y comprensión).

Pensamiento Matemático (operaciones básicas y resolución de problemas razonados vinculados al proyecto).

5. Evaluación y Bibliografía:

Sugerencia de Libros SEP: Cita páginas de Proyectos, Nuestros Saberes y Múltiples Lenguajes.

Examen de {num_preguntas} preguntas: Situacionales con clave.

Instrumentos: Una Rúbrica Formativa y un instrumento adicional (Diario, Escala de Actitudes o Guía de Observación) según el enfoque formativo.

Formato de salida: Utiliza tablas para la dosificación y la secuencia didáctica. Usa negritas para resaltar conceptos clave de la NEM.
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