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
# CSS GLOBAL – UI PREMIUM FCJ
# =============================================
st.markdown(
    """
<style>

html, body, [class*="css"]  {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}

/* Paleta baseada na logo da FCJ */
:root {
    --fcj-primary: #1BA6B2;   /* azul principal */
    --fcj-secondary: #64C7D0; /* azul claro */
    --fcj-deep: #0F5C63;      /* azul profundo */
    --bg-page: #F5F7FA;
    --bg-card: #FFFFFF;
    --border-soft: #E5E7EB;
    --text-dark: #111827;
    --text-gray: #4B5563;
}

/* Forçar fundo light */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-page) !important;
}

/* ===============================
   LAYOUT PRINCIPAL
   =============================== */

.fcj-page {
    padding: 22px 40px 30px 40px;
}

.fcj-main-grid {
    display: grid;
    grid-template-columns: minmax(260px, 340px) minmax(0, 1fr);
    grid-gap: 22px;
    margin-top: 18px;
}

/* ===============================
   HEADER
   =============================== */

.fcj-header-bar {
    background: linear-gradient(90deg, #ffffff 0%, #eafeff 40%, #ffffff 100%);
    border-radius: 18px;
    border: 1px solid var(--border-soft);
    padding: 18px 22px;
    display: flex;
    align-items: center;
}

.fcj-header-badge {
    background-color: #d9f9fc;
    color: var(--fcj-deep);
    font-size: 0.75rem;
    padding: 4px 12px;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

.fcj-header-title {
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 2px;
}

.fcj-header-sub {
    font-size: 0.96rem;
    color: var(--text-gray);
}

/* ===============================
   PANELS
   =============================== */

.fcj-panel {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 16px 18px;
}

.fcj-panel-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-dark);
}

.fcj-panel-sub {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin-top: 6px;
    margin-bottom: 12px;
}

/* ===============================
   CHAT
   =============================== */

.fcj-chat-card {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 18px 20px;
    margin-bottom: 12px;
}

.fcj-chat-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 4px;
}

.fcj-chat-sub {
    font-size: 0.8rem;
    color: var(--text-gray);
    margin-bottom: 12px;
}

/* Mensagens */
.msg-user {
    background: var(--fcj-primary);
    padding: 10px 14px;
    color: white !important;
    border-radius: 14px;
    max-width: 72%;
    margin-left: auto;
    margin-bottom: 10px;
    font-size: 0.94rem;
    box-shadow: 0 6px 12px rgba(27, 166, 178, 0.24);
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d7f1f4;
    padding: 10px 14px;
    color: var(--text-dark) !important;
    border-radius: 14px;
    max-width: 80%;
    margin-bottom: 10px;
    font-size: 0.94rem;
}

/* Inputs e botões */
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
    padding: 8px 24px !important;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(15, 92, 99, 0.22);
}

.stButton > button:hover {
    background: #0c4850 !important;
}

.fcj-footer {
    margin-top: 18px;
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


# Se não preencher identificação → Para tudo
if not founder_id:
    st.stop()


# =============================================
# INÍCIO DA PÁGINA
# =============================================
st.markdown(
    """
<div class="fcj-page">
  <div class="fcj-header-bar">
    <div>
      <div class="fcj-header-badge">Agente de IA • TR4CTION</div>
      <div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>
      <div class="fcj-header-sub">Diagnóstico, ICP, SWOT e Persona com base oficial do TR4CTION.</div>
    </div>
  </div>

  <div class="fcj-main-grid">
""",
    unsafe_allow_html=True,
)


# =============================================
# COLUNA ESQUERDA (ETAPAS)
# =============================================
col_left, col_right = st.columns([0.92, 2.08])

with col_left:
    st.markdown('<div class="fcj-panel">', unsafe_allow_html=True)

    st.markdown('<div class="fcj-panel-title">Etapa do Q1</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fcj-panel-sub">Selecione o bloco atual da trilha TR4CTION.</div>',
        unsafe_allow_html=True,
    )

    step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
    stage_label = st.selectbox("", step_labels, label_visibility="collapsed")
    step_key = LABEL_TO_STEP_KEY[stage_label]

    st.markdown(
        f"""
        <div style="margin-top:12px;font-size:0.86rem;color:#6b7280;">
        <strong>Startup:</strong> {startup_name}<br>
        <strong>Founder:</strong> {founder_name}<br>
        <strong>Etapa atual:</strong> {stage_label}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =============================================
# COLUNA DIREITA – CHAT FINAL (COM LOGO + SEM RETÂNGULO)
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

with col_right:

    # Quando não há mensagens → Exibe logo no centro
    if len(st.session_state.history) == 0:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 0 30px 0;">
                <img src="https://fcjventurebuilder.com/wp-content/uploads/2023/05/logo-fcj-2023-azul.png"
                     style="width:110px; opacity:0.9;">
                <div style="margin-top:12px;font-size:0.95rem;color:#6b7280;">
                    Seu assistente TR4CTION está pronto.<br>
                    Envie uma mensagem para iniciar o atendimento 💬
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # Renderiza o chat somente quando houver mensagens
        st.markdown('<div class="fcj-chat-card">', unsafe_allow_html=True)
        st.markdown('<div class="fcj-chat-title">Conversa com o TR4CTION Agent</div>', unsafe_allow_html=True)

        for msg in st.session_state.history:
            if msg["role"] == "user":
                st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # CAIXA DE MENSAGEM
    user_input = st.text_input("", placeholder="Digite sua pergunta, contexto ou resposta aqui...")

    # ENTER → enviar
    if st.button("Enviar mensagem") or st.session_state.get("last_input") == user_input:
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

    st.markdown(
        """
        <div class="fcj-footer">
            FCJ Venture Builder • TR4CTION Agent – protótipo acadêmico para apoio consultivo-operacional.
        </div>
        """,
        unsafe_allow_html=True,
    )
