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
# ESTILO GLOBAL (FCJ TECH LIGHT)
# =============================================
st.markdown(
    """
<style>

html, body, [class*="css"]  {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}

/* Paleta FCJ */
:root {
    --fcj-primary: #1BA6B2;   /* azul principal FCJ */
    --fcj-secondary: #64C7D0; /* azul claro */
    --fcj-deep: #0F5C63;      /* azul profundo */
    --bg-light: #F5F7FA;
    --text-dark: #111827;
    --text-gray: #4B5563;
}

/* Força app em modo claro */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

/* =============================== */
/* SIDEBAR – BLOCO INSTITUCIONAL   */
/* =============================== */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e5e7eb;
    padding: 22px 20px !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-dark) !important;
}

.sidebar-brand-block {
    background: linear-gradient(135deg, var(--fcj-primary), var(--fcj-secondary));
    border-radius: 16px;
    padding: 14px 14px 10px 14px;
    margin-bottom: 22px;
    color: #ffffff;
}

.sidebar-brand-title {
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    opacity: 0.9;
}

.sidebar-brand-sub {
    font-size: 0.75rem;
    opacity: 0.85;
}

.sidebar-section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-top: 8px;
    margin-bottom: 8px;
}

/* =============================== */
/* HEADER                          */
/* =============================== */
.header-wrapper {
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 10px;
    margin-bottom: 14px;
}

.header-title {
    color: var(--text-dark);
    font-size: 1.7rem;
    font-weight: 700;
}

.header-sub {
    color: var(--text-gray);
    font-size: 0.98rem;
    margin-top: 2px;
}

.header-tag {
    display: inline-block;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: var(--fcj-deep);
    background-color: #e0f7fb;
    padding: 3px 8px;
    border-radius: 999px;
    margin-bottom: 4px;
}

/* =============================== */
/* CHAT                            */
/* =============================== */

.chat-wrapper {
    background-color: #ffffff;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    padding: 18px 18px 8px 18px;
    margin-bottom: 18px;
}

.msg-user {
    background: var(--fcj-primary);
    padding: 10px 14px;
    color: #ffffff !important;
    border-radius: 14px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 10px;
    font-size: 0.94rem;
    box-shadow: 0 6px 12px rgba(27, 166, 178, 0.25);
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d1f0f4;
    padding: 10px 14px;
    color: var(--text-dark) !important;
    border-radius: 14px;
    max-width: 75%;
    margin-bottom: 10px;
    font-size: 0.94rem;
}

/* =============================== */
/* INPUTS & BOTÕES                 */
/* =============================== */

textarea, input {
    background: #ffffff !important;
    color: var(--text-dark) !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
}

.stTextArea textarea {
    min-height: 90px !important;
}

.stButton > button {
    background: var(--fcj-deep) !important;
    color: #ffffff !important;
    border-radius: 999px !important;
    padding: 6px 22px !important;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 10px rgba(15, 92, 99, 0.25);
}

.stButton > button:hover {
    background: #0c4850 !important;
}

/* LABELS */
.stSelectbox label, .stTextInput label {
    font-weight: 500;
    color: var(--text-gray);
}

/* SEÇÃO "Enviar mensagem" */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-top: 8px;
    margin-bottom: 4px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =============================================
# SIDEBAR – IDENTIFICAÇÃO FCJ
# =============================================
with st.sidebar:
    # Bloco institucional com marca FCJ
    st.markdown(
        """
        <div class="sidebar-brand-block">
          <div class="sidebar-brand-title">FCJ Venture Builder</div>
          <div class="sidebar-brand-sub">TR4CTION – Q1 Marketing</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='sidebar-section-title'>Identificação</div>",
        unsafe_allow_html=True,
    )

    startup_name = st.text_input("Startup")
    founder_name = st.text_input("Founder")

    def generate_id(s: str, f: str) -> str:
        return (s + "_" + f).lower().replace(" ", "_")[:60]

    founder_id = None
    if startup_name and founder_name:
        founder_id = generate_id(startup_name, founder_name)
        st.caption(f"ID gerado automaticamente:")
        st.success(founder_id)

        if st.button("🧹 Limpar conversa"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:#6b7280;'>Powered by FCJ Venture Builder • TR4CTION Agent</small>",
        unsafe_allow_html=True,
    )

# Se não tiver identificação, não mostra o resto
if not (startup_name and founder_name and founder_id):
    st.markdown(
        """
        <div style="
            margin-top:80px;
            display:flex;
            justify-content:center;
        ">
          <div style="
            background:#e0f2fe;
            color:#1e3a8a;
            padding:14px 22px;
            border-radius:999px;
            font-size:0.95rem;
          ">
            Preencha <strong>Startup</strong> e <strong>Founder</strong> na lateral para iniciar o atendimento.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# =============================================
# HEADER – FCJ TECH LIGHT
# =============================================
st.markdown(
    """
    <div class="header-wrapper">
      <div class="header-tag">Agente de IA • Q1 TR4CTION</div>
      <div class="header-title">TR4CTION Agent – FCJ Venture Builder</div>
      <div class="header-sub">
        Assistente estratégico para Diagnóstico, ICP, SWOT e Persona, usando o material oficial do TR4CTION.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================
# ETAPAS DO Q1
# =============================================
step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
stage_label = st.selectbox("Etapa atual do Q1", step_labels)
step_key = LABEL_TO_STEP_KEY[stage_label]

# =============================================
# HISTÓRICO DO CHAT
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

st.markdown(
    "<div style='font-weight:600;color:#111827;margin-bottom:6px;'>💬 Conversa</div>",
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# CAIXA DE MENSAGEM
# =============================================
st.markdown("<div class='section-title'>✏️ Enviar mensagem ao agente</div>", unsafe_allow_html=True)
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
