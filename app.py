import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# =============================================
# CONFIG DO APP
# =============================================
st.set_page_config(
    page_title="TR4CTION Agent – FCJ Venture Builder",
    layout="wide",
    page_icon="🚀",
)

# =============================================
# ESTILO GLOBAL (CSS)
# =============================================
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

[data-testid="stAppViewContainer"] {
    background-color: var(--bg-page) !important;
}

.fcj-landing {
    text-align: center;
    padding-top: 80px;
}

.fcj-title-main {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: 3px;
    color: var(--text-dark);
    margin-bottom: 6px;
}

.fcj-subtitle-main {
    font-size: 1rem;
    color: var(--text-gray);
}

.fcj-header-title {
    font-size: 2.1rem;
    margin-top: 10px;
    font-weight: 800;
    text-align: center;
    letter-spacing: 2px;
}

.fcj-header-sub {
    text-align: center;
    font-size: 0.95rem;
    color: var(--text-gray);
    margin-bottom: 16px;
}

.msg-user {
    background: var(--fcj-primary);
    color: #ffffff !important;
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 72%;
    margin-left: auto;
    font-size: 0.94rem;
    box-shadow: 0 4px 12px rgba(27, 166, 178, 0.28);
    margin-bottom: 8px;
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d1f0f4;
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 78%;
    font-size: 0.94rem;
    margin-bottom: 8px;
}

.stTextInput input {
    border-radius: 10px;
}

.stButton > button {
    background: var(--fcj-deep) !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 6px 22px !important;
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
            FCJ VENTURE BUILDER
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

    def generate_id(s: str, f: str) -> str:
        return (s + "_" + f).lower().replace(" ", "_")[:60]

    founder_id = None
    if startup_name and founder_name:
        founder_id = generate_id(startup_name, founder_name)
        st.caption("ID automático:")
        st.success(founder_id)

        if st.button("🧹 Limpar conversa"):
            st.session_state.history = []
            if "input_box" in st.session_state:
                del st.session_state["input_box"]
            st.rerun()

    st.markdown("---")
    st.caption("Powered by FCJ • TR4CTION Q1")


# =============================================
# SE DADOS NÃO ESTÃO PREENCHIDOS → LANDING PAGE
# =============================================
if not (startup_name and founder_name and founder_id):
    st.markdown(
        """
        <div class="fcj-landing">
            <div class="fcj-title-main">FCJ VENTURE BUILDER</div>
            <div class="fcj-subtitle-main">
                TR4CTION Agent – Diagnóstico, ICP, SWOT e Persona<br>
                Preencha os dados da startup no menu lateral para começar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# =============================================
# AGENTE
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

# =============================================
# HEADER
# =============================================
st.markdown(
    """
    <div class="fcj-header-title">FCJ VENTURE BUILDER</div>
    <div class="fcj-header-sub">TR4CTION Agent – Diagnóstico, ICP, SWOT e Persona</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# =============================================
# COLUNAS
# =============================================
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Etapa do Q1")

    step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
    stage_label = st.selectbox("Selecione o bloco atual:", step_labels)
    step_key = LABEL_TO_STEP_KEY[stage_label]

    st.write(f"**Startup:** {startup_name}")
    st.write(f"**Founder:** {founder_name}")
    st.write(f"**Etapa atual:** {stage_label}")


# =============================================
# FUNÇÃO DE ENVIO COM ENTER (CORRIGIDA)
# =============================================
def handle_submit():
    user_text = st.session_state.get("input_box", "").strip()

    if not user_text:
        return

    st.session_state.history.append({"role": "user", "content": user_text})

    response = agent.ask(
        step_key=step_key,
        history=st.session_state.history,
        user_input=user_text,
    )

    st.session_state.history.append({"role": "assistant", "content": response})

    register_answer(
        founder_id=founder_id,
        startup=startup_name,
        founder_name=founder_name,
        step=step_key,
        answer_text=response,
    )

    # limpa corretamente sem gerar erro
    if "input_box" in st.session_state:
        del st.session_state["input_box"]

    st.rerun()


# =============================================
# CHAT
# =============================================
with col_right:
    st.subheader("Conversa com o TR4CTION Agent")

    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("### ✏️ Enviar nova mensagem")

    # Campo com enter para enviar
    st.text_input(
        "",
        placeholder="Digite sua pergunta, contexto ou resposta aqui...",
        key="input_box",
        on_change=handle_submit,
    )

    # Botão opcional
    if st.button("Enviar mensagem"):
        handle_submit()
