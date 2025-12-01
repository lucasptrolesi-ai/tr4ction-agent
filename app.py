import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# ============================================================
# CONFIG DO APP – FCJ CORPORATE TECH
# ============================================================
st.set_page_config(
    page_title="TR4CTION Agent – FCJ Venture Builder",
    layout="wide",
    page_icon="🚀",
)

# ============================================================
# CSS GLOBAL – PALETA FCJ
# ============================================================
st.markdown(
    """
<style>

html, body, [class*="css"] {
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

/* Fundo geral */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-page) !important;
}

/* Landing */
.fcj-landing {
    text-align:center;
    padding-top:70px;
}
.fcj-title-main {
    font-size:42px;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:2px;
    color:#008b99;
}
.fcj-subtitle {
    font-size:1rem;
    margin-top:6px;
    color:var(--text-gray);
}

/* Cards e chat */
.fcj-chat-card {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 14px 16px;
    margin-bottom: 10px;
}

/* Mensagens */
.msg-user {
    background: var(--fcj-primary);
    color: #ffffff;
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 12px;
    font-size: 0.94rem;
    box-shadow: 0 4px 12px rgba(27,166,178,0.25);
}
.msg-agent {
    background: #f0fbfd;
    border:1px solid #d1f0f4;
    color:var(--text-dark);
    padding:10px 14px;
    border-radius:14px;
    max-width:75%;
    margin-bottom:12px;
    font-size:0.94rem;
}

/* Inputs e botões */
.stTextInput input {
    border-radius:10px !important;
    border:1px solid var(--border-soft) !important;
}
.stButton > button {
    background: var(--fcj-deep) !important;
    color:white !important;
    border-radius:20px !important;
    padding:6px 22px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:white !important;
    border-right:1px solid #e5e7eb;
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR – IDENTIFICAÇÃO
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;color:#6b7280;">
                FCJ Venture Builder
            </div>
            <div style="font-size:1.2rem;font-weight:700;color:#111827;">
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
            st.session_state.user_input = ""
            st.rerun()

    st.markdown("---")
    st.caption("Powered by FCJ • TR4CTION Q1")

# ============================================================
# LANDING (caso ainda não tenha identificação)
# ============================================================
if not (startup_name and founder_name and founder_id):
    st.markdown(
        """
        <div class="fcj-landing">
            <h1 class="fcj-title-main">FCJ venture builder</h1>
            <div class="fcj-subtitle">
                Assistente estratégico baseado na metodologia oficial TR4CTION.<br>
                Preencha os dados da startup no menu lateral para começar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ============================================================
# INICIALIZAÇÃO DO AGENTE
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

# ============================================================
# CABEÇALHO PRINCIPAL
# ============================================================
st.markdown(
    """
    <div style="text-align:center; margin-top:10px;">
        <h1 class="fcj-title-main">FCJ VENTURE BUILDER</h1>
        <div class="fcj-subtitle">TR4CTION Agent – Diagnóstico, ICP, SWOT e Persona</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================
# LAYOUT: COLUNA ESQUERDA (ETAPA) + DIREITA (CHAT)
# ============================================================
col_left, col_right = st.columns([1, 2])

# ------------------------------------------------------------
# COLUNA ESQUERDA
# ------------------------------------------------------------
with col_left:
    st.subheader("Etapa do Q1")

    step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
    stage_label = st.selectbox("Selecione o bloco atual:", step_labels)
    step_key = LABEL_TO_STEP_KEY[stage_label]

    st.write(f"**Startup:** {startup_name}")
    st.write(f"**Founder:** {founder_name}")
    st.write(f"**Etapa atual:** {stage_label}")

# ============================================================
# FUNÇÃO DE ENVIO – ENTER + limpar campo
# ============================================================
def handle_submit():
    text = st.session_state.get("user_input", "").strip()
    if not text:
        return

    # adiciona mensagem
    st.session_state.history.append({"role": "user", "content": text})

    # resposta do agente
    response = agent.ask(
        step_key=step_key,
        history=st.session_state.history,
        user_input=text,
    )

    st.session_state.history.append({"role": "assistant", "content": response})

    # salva no dashboard
    register_answer(
        founder_id=founder_id,
        startup=startup_name,
        founder_name=founder_name,
        step=step_key,
        answer_text=response,
    )

    # limpa o campo
    st.session_state.user_input = ""
    st.rerun()

# ============================================================
# COLUNA DIREITA — CHAT
# ============================================================
with col_right:
    st.subheader("Conversa com o TR4CTION Agent")

    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("### ✏️ Enviar nova mensagem")

    st.text_input(
        "",
        key="user_input",
        placeholder="Digite sua pergunta, contexto ou resposta aqui...",
        on_change=handle_submit,
    )

    # Botão opcional
    if st.button("Enviar mensagem"):
        handle_submit()
