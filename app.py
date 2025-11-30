# app.py
import streamlit as st
from agent_core import Tr4ctionAgent

st.set_page_config(
    page_title="Agente TR4CTION - Q1",
    page_icon="🚀",
    layout="wide",
)

st.title("🤖 Agente TR4CTION – Q1 (MVP)")
st.write("Assistente de IA para founders, baseado na trilha TR4CTION da FCJ.")

# Sidebar – configurações básicas
st.sidebar.header("Configurações do Projeto")

startup_name = st.sidebar.text_input(
    "Nome da startup",
    value="Startup Exemplo",
)

step = st.sidebar.selectbox(
    "Etapa do Q1",
    options=[
        ("diagnostico", "Diagnóstico + CSD"),
        ("icp_swot", "ICP + SWOT"),
        ("persona_jtbd", "Persona + JTBD"),
        # Depois a gente adiciona mais:
        # ("jornada_puv", "Jornada + PUV"),
    ],
    format_func=lambda x: x[1],
)

step_key = step[0]

st.sidebar.markdown("---")
st.sidebar.caption("MVP – foco em Q1 com fluxo guiado.")

# Estado de sessão: histórico por etapa
if "chat_history" not in st.session_state:
    # dict: step_key -> list de mensagens
    st.session_state.chat_history = {}

if step_key not in st.session_state.chat_history:
    st.session_state.chat_history[step_key] = []

chat_history = st.session_state.chat_history[step_key]

# Instancia o agente
agent = Tr4ctionAgent(startup_name=startup_name)

# Mostra histórico
st.subheader(f"Etapa atual: {step[1]}")

for msg in chat_history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Input do usuário
user_input = st.chat_input("Digite sua dúvida, informação ou peça ajuda para preencher o template:")

if user_input:
    # adiciona mensagem do usuário no histórico
    chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # chama o agente
    with st.chat_message("assistant"):
        with st.spinner("Pensando como TR4CTION..."):
            answer = agent.ask(
                step_key=step_key,
                history=chat_history[:-1],  # histórico sem a última (já adicionamos como user)
                user_input=user_input,
            )
            st.markdown(answer)

    # adiciona resposta no histórico
    chat_history.append({"role": "assistant", "content": answer})

    # salva de volta no estado
    st.session_state.chat_history[step_key] = chat_history
