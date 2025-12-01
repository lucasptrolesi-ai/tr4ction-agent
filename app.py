import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# =============================================
# CONFIG DO APP – FCJ TECH LIGHT
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

.fcj-landing {
    text-align: center;
    padding-top: 60px;
}

.fcj-logo {
    width: 240px;
    margin-bottom: 22px;
}

.fcj-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-dark);
}

.fcj-subtitle {
    font-size: 1rem;
    color: var(--text-gray);
    margin-top: 6px;
}

.fcj-chat-card {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 14px 16px;
    margin-bottom: 10px;
}

.msg-user {
    background: var(--fcj-primary);
    color: #ffffff !important;
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 72%;
    margin-left: auto;
    margin-bottom: 10px;
    font-size: 0.94rem;
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d1f0f4;
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 78%;
    margin-bottom: 10px;
    font-size: 0.94rem;
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

    def generate_id(s: str, f: str) -> str:
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

# =============================================
# SE AINDA NÃO PREENCHERAM STARTUP/FOUNDER
# =============================================
if not (startup_name and founder_name and founder_id):
    st.markdown(
        """
        <div class="fcj-landing">
            <img src="assets/fcj_logo.png" class="fcj-logo"/>
            <div class="fcj-title">Bem-vindo ao TR4CTION Agent</div>
            <div class="fcj-subtitle">
                Um assistente estratégico baseado na metodologia oficial da FCJ Venture Builder.<br>
                Preencha os dados da startup no menu lateral para iniciar.
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
    <div style="text-align:center;margin-top:10px;">
        <img src="assets/fcj_logo.png" class="fcj-logo"/>
        <div class="fcj-title">TR4CTION Agent – FCJ Venture Builder</div>
        <div class="fcj-subtitle">Diagnóstico, ICP, SWOT e Persona usando a trilha oficial TR4CTION.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# =============================================
# ETAPA + CHAT
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
# FUNÇÃO DE ENVIO (ENTER)
# =============================================
def handle_submit():
    user_text = st.session_state.get("user_input", "").strip()
    if not user_text:
        return

    st.session_state.history.append({"role": "user", "content": user_text})

    response = agent.ask(
        step_key=step_key,
        history=st.session_state.history,
        user_input=user_text,
    )

    st.session_state.history.append(
        {"role": "assistant", "content": response}
    )

    register_answer(
        founder_id=founder_id,
        startup=startup_name,
        founder_name=founder_name,
        step=step_key,
        answer_text=response,
    )

    st.session_state.user_input = ""
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

    # Campo que envia com ENTER
    st.text_input(
        "",
        placeholder="Digite sua pergunta, contexto ou resposta aqui...",
        key="user_input",
        on_change=handle_submit,
    )

    # Botão (opcional, funciona também)
    if st.button("Enviar mensagem"):
        handle_submit()
