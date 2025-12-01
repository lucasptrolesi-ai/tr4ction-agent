import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# =============================================
# CONFIG DO APP – FCJ TECH LIGHT FULL UI
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

/* Paleta baseada na marca FCJ */
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

/* Fundo global */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-page) !important;
}

/* ===============================
   HEADER
   =============================== */
.fcj-header-bar {
    background: linear-gradient(90deg, #ffffff 0%, #ecfbfd 50%, #ffffff 100%);
    border-radius: 18px;
    border: 1px solid var(--border-soft);
    padding: 18px 26px 18px 26px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}

.fcj-header-badge {
    background-color: #dff7fa;
    color: var(--fcj-deep);
    font-size: 0.75rem;
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.fcj-header-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: var(--text-dark);
}

.fcj-header-sub {
    font-size: 1rem;
    color: var(--text-gray);
    margin-top: -6px;
}

/* ===============================
   ESTRUTURA GERAL
   =============================== */
.fcj-page {
    padding: 20px 38px 30px 38px;
}

.fcj-main-grid {
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 20px;
    margin-top: 20px;
}

/* ===============================
   CARD LATERAL (ETAPA)
   =============================== */
.fcj-panel {
    background: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 18px 18px 20px 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}

.fcj-panel-title {
    font-size: 1.08rem;
    font-weight: 600;
    color: var(--text-dark);
}

.fcj-panel-sub {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin-bottom: 12px;
}

/* ===============================
   CHAT
   =============================== */
.fcj-chat-card {
    background: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 20px;
    min-height: 450px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

.fcj-chat-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-dark);
}

.fcj-chat-sub {
    font-size: 0.83rem;
    color: var(--text-gray);
    margin-bottom: 12px;
}

/* Bolhas do chat */
.msg-user {
    background: var(--fcj-primary);
    padding: 12px 15px;
    color: white !important;
    border-radius: 14px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 12px;
    box-shadow: 0 6px 14px rgba(27,166,178,0.25);
    font-size: 0.94rem;
}

.msg-agent {
    background: #e8f7f9;
    padding: 12px 15px;
    border: 1px solid #b5e4e9;
    color: var(--text-dark) !important;
    border-radius: 14px;
    max-width: 80%;
    margin-bottom: 12px;
    font-size: 0.94rem;
}

/* ===============================
   INPUTS & BOTÕES
   =============================== */
textarea, input {
    background: white !important;
    color: var(--text-dark) !important;
    border: 1px solid #d0d7de !important;
    border-radius: 10px !important;
}

.stTextArea textarea {
    min-height: 90px !important;
}

.stButton > button {
    background: var(--fcj-primary) !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 8px 28px !important;
    border: none;
    box-shadow: 0 6px 14px rgba(27,166,178,0.25);
    font-weight: 600;
    font-size: 0.95rem;
}

.stButton > button:hover {
    background: var(--fcj-deep) !important;
}

/* Rodapé */
.fcj-footer {
    margin-top: 20px;
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
        <div style="margin-bottom:16px;">
          <div style="
            font-size:0.85rem;
            text-transform:uppercase;
            letter-spacing:0.08em;
            color:#6b7280;">
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

    def generate_id(s: str, f: str):
        return (s + "_" + f).lower().replace(" ", "_")[:60]

    founder_id = None
    if startup_name and founder_name:
        founder_id = generate_id(startup_name, founder_name)
        st.caption("ID gerado automaticamente:")
        st.success(founder_id)

        if st.button("🧹 Limpar conversa"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:#6b7280;'>Powered by FCJ Venture Builder • TR4CTION Q1</small>",
        unsafe_allow_html=True,
    )

# Se não estiver identificado → mostra aviso
if not (startup_name and founder_name and founder_id):
    st.markdown(
        """
        <div class="fcj-page">
          <div class="fcj-header-bar">
            <div>
              <div class="fcj-header-badge">Agente de IA • TR4CTION</div>
              <div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>
              <div class="fcj-header-sub">
                Preencha Startup e Founder na barra lateral para iniciar.
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# =============================================
# INÍCIO DA PÁGINA – HEADER COMPLETO
# =============================================
st.markdown(
    """
<div class="fcj-page">

  <div class="fcj-header-bar">
    <div>
      <div class="fcj-header-badge">Agente de IA • TR4CTION</div>
      <div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>
      <div class="fcj-header-sub">
        Assistente estratégico para Diagnóstico, ICP, SWOT e Persona usando o material oficial do TR4CTION.
      </div>
    </div>
  </div>

  <div class="fcj-main-grid">
    """,
    unsafe_allow_html=True,
)

# =============================================
# PAINEL ESQUERDO (ETAPA)
# =============================================
col_left, col_right = st.columns([0.95, 2.05])

with col_left:
    st.markdown('<div class="fcj-panel">', unsafe_allow_html=True)

    st.markdown('<div class="fcj-panel-title">Etapa do Q1</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fcj-panel-sub">Selecione qual bloco você está trabalhando.</div>',
        unsafe_allow_html=True,
    )

    step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
    stage_label = st.selectbox("", step_labels, label_visibility="collapsed")
    step_key = LABEL_TO_STEP_KEY[stage_label]

    st.markdown(
        f"""
        <div style="margin-top:16px;font-size:0.86rem;color:#6b7280;">
            <strong>Startup:</strong> {startup_name}<br>
            <strong>Founder:</strong> {founder_name}<br>
            <strong>Etapa:</strong> {stage_label}
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

    st.markdown('<div class="fcj-chat-title">Conversa com o TR4CTION Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="fcj-chat-sub">Aprofunde a etapa atual conversando com o agente.</div>', unsafe_allow_html=True)

    # Histórico
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input
    user_input = st.text_area("", placeholder="Descreva sua dúvida ou etapa atual...")

    if st.button("Enviar mensagem"):
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

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# RODAPÉ
# =============================================
st.markdown(
    """
    </div> <!-- grid -->
    <div class="fcj-footer">
        FCJ Venture Builder • TR4CTION Agent – protótipo acadêmico para apoio consultivo-operacional.
    </div>
</div> <!-- page -->
""",
    unsafe_allow_html=True,
)
