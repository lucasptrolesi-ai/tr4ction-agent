import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# =============================================
# CONFIGURAÇÃO DO APP (tema premium FCJ)
# =============================================
st.set_page_config(
    page_title="TR4CTION Agent – FCJ Venture Builder",
    layout="wide",
    page_icon="🚀",
)

# CUSTOM CSS
st.markdown("""
<style>

body {
    background-color: #0d1117;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #0d1117;
    padding: 20px;
    border-right: 1px solid #1f2937;
}

.sidebar-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #60a5fa;
    margin-bottom: 12px;
}

.fcj-logo {
    width: 170px;
    margin-bottom: 20px;
}

/* HEADER */
.header-title {
    color: #93c5fd;
    font-size: 2rem;
    font-weight: 700;
}

.header-sub {
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-top: -10px;
}

/* BALOES DO CHAT */
.msg-user {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    padding: 14px;
    color: white;
    border-radius: 12px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 12px;
}

.msg-agent {
    background: #1f2937;
    border: 1px solid #374151;
    padding: 14px;
    color: #e5e7eb;
    border-radius: 12px;
    max-width: 75%;
    margin-bottom: 12px;
}

/* CAIXA DE TEXTO */
textarea {
    background: #0f172a !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

/* BOTÃO */
button[kind="primary"] {
    background: #2563eb !important;
    color: white !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)


# =============================================
# SIDEBAR PREMIUM FCJ
# =============================================
with st.sidebar:
    st.image("https://fcjventurebuilder.com/wp-content/uploads/2023/05/logo-fcj-2023-branca.png",
             use_column_width=True)

    st.markdown("<div class='sidebar-title'>Identificação</div>", unsafe_allow_html=True)

    startup_name = st.text_input("Startup")
    founder_name = st.text_input("Founder")

    def generate_id(s, f):
        return (s + "_" + f).lower().replace(" ", "_")[:60]

    if startup_name and founder_name:
        founder_id = generate_id(startup_name, founder_name)
        st.success(f"ID: {founder_id}")

        if st.button("Limpar conversa"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown("<small style='color:#64748b;'>Powered by FCJ Venture Builder • TR4CTION Q1</small>", unsafe_allow_html=True)


# Se não tiver identificação, trava.
if not (startup_name and founder_name):
    st.stop()


# =============================================
# HEADER PREMIUM
# =============================================
st.markdown("<div class='header-title'>🚀 TR4CTION Agent — FCJ Venture Builder</div>",
            unsafe_allow_html=True)

st.markdown("<div class='header-sub'>Assistente Estratégico para Diagnóstico, ICP, SWOT e Persona</div>",
            unsafe_allow_html=True)
st.markdown("")


# =============================================
# ETAPAS (SELECT)
# =============================================
step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
stage_label = st.selectbox("Selecione a etapa:", step_labels)
step_key = LABEL_TO_STEP_KEY[stage_label]

st.markdown("")


# =============================================
# HISTÓRICO
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)


# =============================================
# ÁREA DE CHAT
# =============================================
st.markdown("## 💬 Chat")

chat_container = st.container()

with chat_container:
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)


# =============================================
# ENTRADA DO FUNDER
# =============================================
st.markdown("## ✏️ Enviar mensagem")
user_input = st.text_area("", placeholder="Digite aqui sua mensagem...")

if st.button("Enviar"):
    if user_input.strip():
        st.session_state.history.append({"role": "user", "content": user_input})
        
        response = agent.ask(
            step_key=step_key,
            history=st.session_state.history,
            user_input=user_input
        )
        
        st.session_state.history.append({"role": "assistant", "content": response})
        
        register_answer(
            founder_id=founder_id,
            startup=startup_name,
            founder_name=founder_name,
            step=step_key,
            answer_text=response
        )

        st.rerun()
