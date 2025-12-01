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

/* Forçar fundo claro geral */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-page) !important;
}

/* ===============================
   LAYOUT PRINCIPAL
   =============================== */

.fcj-page {
    padding: 20px 40px 30px 40px;
}

.fcj-main-grid {
    display: grid;
    grid-template-columns: minmax(260px, 340px) minmax(0, 1fr);
    grid-gap: 18px;
    margin-top: 18px;
}

/* ===============================
   HEADER
   =============================== */

.fcj-header-bar {
    background: linear-gradient(90deg, #ffffff 0%, #f0fbfd 40%, #ffffff 100%);
    border-radius: 18px;
    border: 1px solid var(--border-soft);
    padding: 16px 22px 14px 22px;
    display: flex;
    align-items: center;
    gap: 14px;
}

.fcj-header-badge {
    background-color: #e0f7fb;
    color: var(--fcj-deep);
    font-size: 0.75rem;
    padding: 4px 10px;
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
   CARD LATERAL (ETAPA / INFO)
   =============================== */

.fcj-panel {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 16px 16px 18px 16px;
}

.fcj-panel-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 4px;
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
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 14px 16px 10px 16px;
}

.fcj-chat-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 6px;
}

.fcj-chat-sub {
    font-size: 0.8rem;
    color: var(--text-gray);
    margin-bottom: 10px;
}

/* Balões */
.msg-user {
    background: var(--fcj-primary);
    padding: 10px 14px;
    color: #ffffff !important;
    border-radius: 14px;
    max-width: 72%;
    margin-left: auto;
    margin-bottom: 10px;
    font-size: 0.94rem;
    box-shadow: 0 6px 12px rgba(27, 166, 178, 0.24);
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d1f0f4;
    padding: 10px 14px;
    color: var(--text-dark) !important;
    border-radius: 14px;
    max-width: 78%;
    margin-bottom: 10px;
    font-size: 0.94rem;
}

/* ===============================
   INPUTS E BOTÕES
   =============================== */

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
    box-shadow: 0 4px 10px rgba(15, 92, 99, 0.22);
}

.stButton > button:hover {
    background: #0c4850 !important;
}

/* Labels dos campos */
.stSelectbox label, .stTextInput label {
    font-weight: 500;
    color: var(--text-gray);
}

/* Rodapé leve */
.fcj-footer {
    margin-top: 12px;
    font-size: 0.78rem;
    color: #9ca3af;
    text-align: right;
}

</style>
""",
    unsafe_allow_html=True,
)

# =============================================
# SIDEBAR – SÓ IDENTIFICAÇÃO (MANTIDA SIMPLES)
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

    def generate_id(s: str, f: str) -> str:
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

# Se não tiver identificação, só mostra o aviso no centro
if not (startup_name and founder_name and founder_id):
    st.markdown(
        """
        <div class="fcj-page">
          <div class="fcj-header-bar">
            <div>
              <div class="fcj-header-badge">Agente de IA • Q1 TR4CTION</div>
              <div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>
              <div class="fcj-header-sub">
                Preencha os campos de <strong>Startup</strong> e <strong>Founder</strong> na lateral para iniciar.
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# =============================================
# INÍCIO DA PÁGINA – HTML ESTRUTURADO
# =============================================
st.markdown(
    """
<div class="fcj-page">

  <div class="fcj-header-bar">
    <div>
      <div class="fcj-header-badge">Agente de IA • Q1 TR4CTION</div>
      <div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>
      <div class="fcj-header-sub">
        Assistente estratégico para orientar o founder no Diagnóstico, ICP, SWOT e Persona,
        usando o material oficial da trilha TR4CTION.
      </div>
    </div>
  </div>

  <div class="fcj-main-grid">
"""
    ,
    unsafe_allow_html=True,
)

# =============================================
# COLUNA ESQUERDA – ETAPA + CONTEXTO
# =============================================
col_left, col_right = st.columns([0.95, 2.05])

with col_left:
    st.markdown('<div class="fcj-panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="fcj-panel-title">Etapa do Q1</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="fcj-panel-sub">Selecione qual bloco da trilha TR4CTION você está trabalhando agora.</div>',
        unsafe_allow_html=True,
    )

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

    st.markdown(
        """
        <div style="margin-top:14px;font-size:0.8rem;color:#9ca3af;">
          Dica: responda com exemplos reais. O agente vai fazer perguntas antes de sugerir preenchimentos.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# COLUNA DIREITA – CHAT COMPLETO
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

with col_right:
    # Card do chat
    st.markdown('<div class="fcj-chat-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="fcj-chat-title">Conversa com o TR4CTION Agent</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="fcj-chat-sub">Use o chat para aprofundar as respostas da etapa atual. O agente usa o material oficial do TR4CTION como base.</div>',
        unsafe_allow_html=True,
    )

    # Renderiza histórico
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

    # Caixa de mensagem
    st.markdown(
        "<div style='margin-top:12px;font-weight:500;color:#111827;font-size:0.95rem;'>✏️ Enviar nova mensagem</div>",
        unsafe_allow_html=True,
    )
    user_input = st.text_area(
        "",
        placeholder="Descreva sua situação, dúvida ou próxima etapa que deseja trabalhar...",
    )

    if st.button("Enviar mensagem"):
        if user_input.strip():
            # adiciona ao histórico
            st.session_state.history.append({"role": "user", "content": user_input})

            # chama o agente
            response = agent.ask(
                step_key=step_key,
                history=st.session_state.history,
                user_input=user_input,
            )

            st.session_state.history.append(
                {"role": "assistant", "content": response}
            )

            # salva para o dashboard
            register_answer(
                founder_id=founder_id,
                startup=startup_name,
                founder_name=founder_name,
                step=step_key,
                answer_text=response,
            )

            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# FECHA DIV PRINCIPAL E RODAPÉ
# =============================================
st.markdown(
    """
  </div> <!-- fcj-main-grid -->

  <div class="fcj-footer">
    FCJ Venture Builder · TR4CTION Agent – protótipo acadêmico para apoio consultivo-operacional.
  </div>

</div> <!-- fcj-page -->
""",
    unsafe_allow_html=True,
)
