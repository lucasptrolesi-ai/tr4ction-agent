import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# =============================================
# CONFIG DO APP – CLEAN CORPORATE
# =============================================
st.set_page_config(
    page_title="TR4CTION Agent – FCJ Venture Builder",
    layout="wide",
    page_icon="🚀",
)

# =============================================
# ESTILO CLEAN GLOBAL
# =============================================
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: "Inter", sans-serif;
}

/* Paleta */
:root {
    --primary-blue: #3b82f6;
    --light-blue: #e8f0fe;
    --light-gray: #f4f4f5;
    --text-dark: #111827;
    --text-gray: #374151;
}

/* Forçar app claro */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

/* SIDEBAR CLEAN */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e5e7eb;
    padding: 20px !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-dark) !important;
}

.sidebar-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--primary-blue) !important;
    margin-bottom: 12px;
}

/* HEADER */
.header-title {
    color: var(--text-dark) !important;
    font-size: 2rem;
    font-weight: 700;
}

.header-sub {
    color: var(--text-gray) !important;
    font-size: 1.05rem;
    margin-top: -6px;
}

/* BALÕES DO CHAT */
.msg-user {
    background: var(--primary-blue);
    padding: 12px 16px;
    color: #ffffff !important;
    border-radius: 14px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 12px;
    font-size: 0.95rem;
}

.msg-agent {
    background: var(--light-blue);
    padding: 12px 16px;
    color: var(--text-dark) !important;
    border-radius: 14px;
    max-width: 75%;
    margin-bottom: 12px;
    font-size: 0.95rem;
}

/* INPUTS */
textarea, input {
    background: #ffffff !important;
    color: var(--text-dark) !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
}

/* BOTÃO */
.stButton > button {
    background-color: var(--primary-blue) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR CLEAN CORPORATE
# =============================================
with st.sidebar:
    # Logo FCJ (troque a URL se quiser usar outra imagem)
    st.image(
        "https://i.imgur.com/YX7FqSR.png",
        use_column_width=True,
    )

    st.markdown("<div class='sidebar-title'>Identificação</div>", unsafe_allow_html=True)

    startup_name = st.text_input("Startup")
    founder_name = st.text_input("Founder")

    def generate_id(s: str, f: str) -> str:
        return (s + "_" + f).lower().replace(" ", "_")[:60]

    founder_id = None
    if startup_name and founder_name:
        founder_id = generate_id(startup_name, founder_name)
        st.success(f"ID: {founder_id}")

        if st.button("Limpar conversa"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:#6b7280;'>Powered by FCJ Venture Builder • TR4CTION Q1</small>",
        unsafe_allow_html=True,
    )

# Se não tiver identificação, não mostra o resto
if not (startup_name and founder_name and founder_id):
    st.info("Preencha Startup e Founder na lateral para iniciar o atendimento.")
    st.stop()

# =============================================
# HEADER
# =============================================
st.markdown(
    "<div class='header-title'>🚀 TR4CTION Agent – FCJ Venture Builder</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='header-sub'>Assistente estratégico para Diagnóstico, ICP, SWOT e Persona no Q1</div>",
    unsafe_allow_html=True,
)
st.markdown("")

# =============================================
# ETAPAS
# =============================================
step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
stage_label = st.selectbox("Selecione a etapa:", step_labels)
step_key = LABEL_TO_STEP_KEY[stage_label]

st.markdown("")

# =============================================
# HISTÓRICO DO CHAT
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

st.markdown("## 💬 Conversa")

chat_container = st.container()

with chat_container:
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='msg-user'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='msg-agent'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )

# =============================================
# CAIXA DE MENSAGEM
# =============================================
st.markdown("## ✏️ Enviar mensagem")
user_input = st.text_area("", placeholder="Digite sua mensagem aqui...")

if st.button("Enviar"):
    if user_input.strip():
        # registra mensagem do founder
        st.session_state.history.append({"role": "user", "content": user_input})

        # consulta o agente
        response = agent.ask(
            step_key=step_key,
            history=st.session_state.history,
            user_input=user_input,
        )

        # registra resposta do agente
        st.session_state.history.append({"role": "assistant", "content": response})

        # persiste no JSON para o dashboard
        register_answer(
            founder_id=founder_id,
            startup=startup_name,
            founder_name=founder_name,
            step=step_key,
            answer_text=response,
        )

        st.rerun()
