import streamlit as st
import os
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# =============================================
# CONFIGURAÇÃO DO APP
# =============================================
st.set_page_config(
    page_title="TR4CTION Agent – FCJ Venture Builder",
    layout="wide",
    page_icon="🚀",
)

# Caminho absoluto para a logo local
LOGO_PATH = os.path.join("assets", "fcj_logo.png")

# =============================================
# CSS – TEMA PREMIUM FCJ
# =============================================
st.markdown(
    """
<style>

html, body, [class*="css"]  {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}

:root {
    --fcj-primary: #1BA6B2;
    --fcj-secondary: #64C7D0;
    --fcj-deep: #0F5C63;
    --bg-page: #F5F7FA;
    --bg-card: #FFFFFF;
    --border-soft: #E5E7EB;
    --text-dark: #111827;
    --text-gray: #4B5563;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg-page) !important;
}

.fcj-page {
    padding: 25px 40px 40px 40px;
}

.fcj-main-grid {
    display: grid;
    grid-template-columns: minmax(260px, 320px) minmax(0, 1fr);
    grid-gap: 26px;
    margin-top: 25px;
}

.fcj-panel {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 18px 20px;
}

.fcj-panel-title {
    font-size: 1.08rem;
    font-weight: 600;
    color: var(--text-dark);
}

.fcj-panel-sub {
    color: var(--text-gray);
    font-size: 0.86rem;
    margin-bottom: 10px;
}

.fcj-chat-card {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 18px 20px;
    margin-bottom: 18px;
}

.msg-user {
    background: var(--fcj-primary);
    color: white !important;
    padding: 12px 16px;
    border-radius: 14px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 12px;
    font-size: 0.96rem;
    box-shadow: 0 6px 12px rgba(27, 166, 178, 0.28);
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d6f4f7;
    color: var(--text-dark) !important;
    padding: 12px 16px;
    border-radius: 14px;
    max-width: 78%;
    margin-bottom: 12px;
    font-size: 0.96rem;
}

textarea, input {
    background: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #d1d5db !important;
}

.stButton > button {
    background: var(--fcj-deep) !important;
    color: white !important;
    padding: 8px 26px !important;
    border-radius: 999px !important;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(15, 92, 99, 0.22);
}

.stButton > button:hover {
    background: #0D4A52 !important;
}

.fcj-landing {
    text-align: center;
    padding: 80px 0 40px 0;
}

.fcj-landing-text {
    margin-top: 18px;
    font-size: 1rem;
    color: var(--text-gray);
}

.fcj-footer {
    margin-top: 30px;
    font-size: 0.78rem;
    color: #9ca3af;
    text-align: right;
}

</style>
""",
    unsafe_allow_html=True,
)

# =============================================
# SIDEBAR – IDENTIFICAÇÃO
# =============================================
with st.sidebar:
    st.markdown(
        """
        <div style="margin-bottom:22px;">
            <div style="font-size:0.85rem;text-transform:uppercase;color:#6b7280;">
                FCJ Venture Builder
            </div>
            <div style="font-size:1.15rem;font-weight:700;color:#111827;">
                TR4CTION Agent
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    startup_name = st.text_input("Startup")
    founder_name = st.text_input("Founder")

    def generate_id(s, f):
        return (s + "_" + f).lower().replace(" ", "_")[:60]

    founder_id = None
    if startup_name and founder_name:
        founder_id = generate_id(startup_name, founder_name)
        st.caption("ID automático:")
        st.success(founder_id)

        if st.button("🧹 Limpar conversa"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown("<small style='color:#6b7280;'>Powered by FCJ • TR4CTION Q1</small>", unsafe_allow_html=True)

if not founder_id:
    st.stop()

# =============================================
# LAYOUT PRINCIPAL
# =============================================
st.markdown("<div class='fcj-page'>", unsafe_allow_html=True)
col_left, col_right = st.columns([0.9, 2.1])

# =============================================
# ETAPA (COLUNA ESQUERDA)
# =============================================
with col_left:
    st.markdown("<div class='fcj-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='fcj-panel-title'>Etapa do Q1</div>", unsafe_allow_html=True)

    step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
    stage_label = st.selectbox("", step_labels, label_visibility="collapsed")
    step_key = LABEL_TO_STEP_KEY[stage_label]

    st.markdown(
        f"""
        <div style="margin-top:14px;font-size:0.86rem;color:#6b7280;">
        <strong>Startup:</strong> {startup_name}<br>
        <strong>Founder:</strong> {founder_name}<br>
        <strong>Etapa atual:</strong> {stage_label}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# CHAT E LOGO CORPORATIVA (COLUNA DIREITA)
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

with col_right:

    # TELA DE APRESENTAÇÃO (Landing)
    if len(st.session_state.history) == 0:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=260)
        else:
            st.error("⚠ Logo não encontrada em /assets/fcj_logo.png")

        st.markdown(
            """
            <div class='fcj-landing-text'>
                <strong>Bem-vindo ao TR4CTION Agent.</strong><br>
                Seu assistente estratégico oficial da trilha FCJ Venture Builder.<br><br>
                Envie sua primeira mensagem para iniciar o atendimento. 💬
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown("<div class='fcj-chat-card'>", unsafe_allow_html=True)

        for msg in st.session_state.history:
            if msg["role"] == "user":
                st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # INPUT
    user_input = st.text_input("", placeholder="Digite sua pergunta ou resposta aqui...")

    if (
        st.button("Enviar mensagem")
        or (st.session_state.get("last_input") == user_input and user_input.strip() != "")
    ):
        if user_input.strip():
            st.session_state.history.append({"role": "user", "content": user_input})

            response = agent.ask(
                step_key=step_key,
                history=st.session_state.history,
                user_input=user_input,
            )

            st.session_state.history.append({"role": "assistant", "content": response})

            register_answer(
                founder_id=founder_id,
                startup=startup_name,
                founder_name=founder_name,
                step=step_key,
                answer_text=response,
            )

            st.session_state.last_input = ""
            st.experimental_rerun()

st.markdown("<div class='fcj-footer'>FCJ Venture Builder • TR4CTION Agent</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
