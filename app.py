import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer
import os

# =============================================
# CONFIG DO APP – FCJ TECH LIGHT UI
# =============================================
st.set_page_config(
    page_title="TR4CTION Agent – FCJ Venture Builder",
    layout="wide",
    page_icon="🚀",
)

# =============================================
# ESTILO GLOBAL (HTML + CSS)
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

/* HEADER */
.fcj-header {
    text-align: center;
    padding: 40px 10px 30px 10px;
}

.fcj-header img {
    max-width: 260px;
    margin-bottom: 20px;
}

.fcj-header-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text-dark);
}

.fcj-header-sub {
    font-size: 1rem;
    color: var(--text-gray);
    margin-top: 6px;
}

/* GRID PRINCIPAL */
.fcj-main-grid {
    display: grid;
    grid-template-columns: minmax(320px, 380px) minmax(0, 1fr);
    grid-gap: 22px;
    margin-top: 10px;
}

/* PANELS */
.fcj-panel {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 20px;
}

.fcj-panel-title {
    font-size: 1.08rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 4px;
}

.fcj-panel-sub {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin-bottom: 14px;
}

/* CHAT */
.fcj-chat-card {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 18px;
}

.msg-user {
    background: var(--fcj-primary);
    padding: 10px 14px;
    color: #fff !important;
    border-radius: 14px;
    max-width: 72%;
    margin-left: auto;
    margin-bottom: 10px;
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d1f0f4;
    padding: 10px 14px;
    color: var(--text-dark) !important;
    border-radius: 14px;
    max-width: 80%;
    margin-bottom: 10px;
}

textarea, input {
    background: #ffffff !important;
    color: var(--text-dark) !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
}

.stButton > button {
    background: var(--fcj-deep) !important;
    color: #ffffff !important;
    border-radius: 999px !important;
    padding: 6px 22px !important;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: #0c4850 !important;
}

.fcj-footer {
    margin-top: 22px;
    font-size: 0.8rem;
    color: #9ca3af;
    text-align: center;
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
        <div style="margin-bottom:18px;">
            <div style="font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;color:#6b7280;">
                FCJ Venture Builder
            </div>
            <div style="font-size:1.1rem;font-weight:700;color:#111827;">
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
    st.markdown(
        "<small style='color:#6b7280;'>Powered by FCJ • TR4CTION Q1</small>",
        unsafe_allow_html=True,
    )

# =============================================
# LANDING SE NÃO PREENCHER OS CAMPOS
# =============================================
if not (startup_name and founder_name):
    st.markdown(
        """
        <div class="fcj-header">
            <img src="assets/fcj_logo.png">
            <div class="fcj-header-title">Bem-vindo ao TR4CTION Agent</div>
            <div class="fcj-header-sub">
                Um assistente estratégico baseado na metodologia oficial da FCJ Venture Builder.<br>
                Preencha os dados da sua startup no menu lateral para iniciar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# =============================================
# CABEÇALHO INTERNO
# =============================================
st.markdown(
    """
    <div class="fcj-header">
        <img src="assets/fcj_logo.png">
        <div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>
        <div class="fcj-header-sub">
            Diagnóstico, ICP, SWOT e Persona usando a trilha oficial TR4CTION.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================
# GRID PRINCIPAL
# =============================================
st.markdown('<div class="fcj-main-grid">', unsafe_allow_html=True)

# =============================================
# COLUNA ESQUERDA – ETAPA
# =============================================
col_left, col_right = st.columns([0.95, 2.05])

with col_left:
    st.markdown('<div class="fcj-panel">', unsafe_allow_html=True)

    st.markdown('<div class="fcj-panel-title">Etapa do Q1</div>', unsafe_allow_html=True)
    st.markdown('<div class="fcj-panel-sub">Selecione o bloco atual da trilha TR4CTION.</div>',
                unsafe_allow_html=True)

    step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
    stage_label = st.selectbox("", step_labels, label_visibility="collapsed")
    step_key = LABEL_TO_STEP_KEY[stage_label]

    st.markdown(
        f"""
        <div style="margin-top:10px;font-size:0.86rem;color:#6b7280;">
            <strong>Startup:</strong> {startup_name}<br>
            <strong>Founder:</strong> {founder_name}<br>
            <strong>Etapa atual:</strong> {stage_label}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# COLUNA DIREITA – CHAT
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

with col_right:
    st.markdown('<div class="fcj-chat-card">', unsafe_allow_html=True)

    # Histórico
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)

    # Caixa de mensagem
    st.markdown(
        "<div style='margin-top:18px;font-weight:500;color:#111827;'>✏️ Enviar nova mensagem</div>",
        unsafe_allow_html=True,
    )

    user_input = st.text_area("", placeholder="Digite sua pergunta, contexto ou resposta aqui...")

    if st.button("Enviar mensagem"):
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

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# RODAPÉ
# =============================================
st.markdown(
    """
    <div class="fcj-footer">
        FCJ Venture Builder · TR4CTION Agent – protótipo acadêmico e consultivo-operacional.
    </div>
    """,
    unsafe_allow_html=True,
)
