
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Asistente Academico IA")
st.title(" Asistente Academico IA")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

INSTRUCCIONES_ASISTENTE = """
Eres un asistente academico especializado
en Ingenieria de Sistemas e Ingenieria
de Software.
Debes orientar a los estudiantes sobre:
- Proyectos
- Evaluaciones
- Investigacion
- Desarrollo de software
- Horarios academicos
Responde de forma profesional.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for mensaje in st.session_state.messages:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

consulta = st.chat_input("Escribe tu consulta académica...")

if consulta:
    st.session_state.messages.append({"role": "user", "content": consulta})
    with st.chat_message("user"):
        st.markdown(consulta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            respuesta = client.responses.create(
                model="openai/gpt-oss-20b",
                instructions=INSTRUCCIONES_ASISTENTE,
                input=st.session_state.messages,
            )
            texto_respuesta = respuesta.output_text
            st.markdown(texto_respuesta)

    st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
