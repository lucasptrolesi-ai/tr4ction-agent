import streamlit as st
from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer

# =============================================
# CONFIG DO APP – FCJ UI
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

/* Paleta baseada na FCJ */
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

/* =========================================
   HEADER
   ========================================= */
.fcj-header-bar {
    background: linear-gradient(90deg, #ffffff 0%, #f0fbfd 40%, #ffffff 100%);
    border-radius: 18px;
    border: 1px solid var(--border-soft);
    padding: 16px 22px;
    margin-bottom: 14px;
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
}

.fcj-header-sub {
    font-size: 0.95rem;
    color: var(--text-gray);
}

/* =========================================
   PAINEL LATERAL
   ========================================= */
.fcj-panel {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 16px;
}

/* =========================================
   CHAT
   ========================================= */
.fcj-chat-card {
    background-color: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-soft);
    padding: 14px 16px;
    min-height: 320px;
    max-height: 520px;
    overflow-y: auto;
}

/* Balões */
.msg-user {
    background: var(--fcj-primary);
    padding: 10px 14px;
    color: #ffffff !important;
    border-radius: 16px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 10px;
    box-shadow: 0 6px 10px rgba(27,166,178,0.22);
}

.msg-agent {
    background: #f0fbfd;
    border: 1px solid #d1f0f4;
    padding: 10px 14px;
    color: var(--text-dark);
    border-radius: 16px;
    max-width: 75%;
    margin-bottom: 10px;
}

/* Placeholder Elegante */
.fcj-chat-empty {
    text-align:center;
    padding:60px 20px;
    color:#6b7280;
}

/* Inputs */
textarea, input {
    border-radius: 10px !important;
    border: 1px solid #d1d5db !important;
}

.stButton > button {
    background: var(--fcj-deep) !important;
    color: white !important;
    padding: 8px 22px !important;
    border-radius: 999px !important;
    font-weight: 600;
    border: none;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
}

</style>
""",
    unsafe_allow_html=True,
)

# =============================================
# JAVASCRIPT — ENTER PARA ENVIAR
# =============================================
st.markdown("""
<script>
document.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        const sendButton = window.parent.document.querySelector('button[kind="primary"]');
        if (sendButton) sendButton.click();
        e.preventDefault();
    }
});
</script>
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR – IDENTIFICAÇÃO
# =============================================
with st.sidebar:
    st.markdown(
        """
        <div style="margin-bottom:18px;">
          <div style="font-size:0.85rem; text-transform:uppercase; color:#6b7280;">
            FCJ Venture Builder
          </div>
          <div style="font-size:1.1rem; font-weight:700; color:#111827;">
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

        if st.button(" Limpar conversa"):
            st.session_state.history = []
            st.rerun()

    st.markdown("---")
    st.markdown("<small style='color:#6b7280;'>Powered by FCJ • TR4CTION Q1</small>", unsafe_allow_html=True)

# =============================================
# BLOQUEAR TELA ATÉ IDENTIFICAÇÃO
# =============================================
if not (startup_name and founder_name and founder_id):
    st.markdown(
        """
        <div class="fcj-header-bar">
            <div class="fcj-header-badge">Agente de IA • Q1</div>
            <div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>
            <div class="fcj-header-sub">
                Preencha <strong>Startup</strong> e <strong>Founder</strong> na lateral esquerda para iniciar.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# =============================================
# LAYOUT PRINCIPAL
# =============================================
st.markdown('<div class="fcj-header-bar">', unsafe_allow_html=True)
st.markdown('<div class="fcj-header-badge">Agente de IA • TR4CTION</div>', unsafe_allow_html=True)
st.markdown('<div class="fcj-header-title">TR4CTION Agent – FCJ Venture Builder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="fcj-header-sub">Diagnóstico, ICP, SWOT e Persona com base oficial do TR4CTION.</div>',
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

col_left, col_right = st.columns([0.95, 2.05])

# =============================================
# COLUNA ESQUERDA — ETAPA
# =============================================
with col_left:
    st.markdown('<div class="fcj-panel">', unsafe_allow_html=True)

    st.markdown("<div class='fcj-panel-title'>Etapa do Q1</div>", unsafe_allow_html=True)
    st.markdown("<div class='fcj-panel-sub'>Selecione o bloco atual da trilha TR4CTION.</div>", unsafe_allow_html=True)

    step_labels = [STEP_CONFIG[k]["label"] for k in STEP_ORDER]
    stage_label = st.selectbox("", step_labels, label_visibility="collapsed")
    step_key = LABEL_TO_STEP_KEY[stage_label]

    st.markdown(
        f"""
        <div style="margin-top:10px;font-size:0.85rem;color:#4B5563;">
            <strong>Startup:</strong> {startup_name}<br>
            <strong>Founder:</strong> {founder_name}<br>
            <strong>Etapa atual:</strong> {stage_label}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# COLUNA DIREITA — CHAT
# =============================================
if "history" not in st.session_state:
    st.session_state.history = []

agent = Tr4ctionAgent(startup_name)

with col_right:

    st.markdown('<div class="fcj-chat-card">', unsafe_allow_html=True)

    if len(st.session_state.history) == 0:
        st.markdown(
            """
            <div class="fcj-chat-empty">
                <img src="https://fcjventurebuilder.com/wp-content/uploads/2023/05/logo-fcj-2023-azul.png"
                     style="width:160px; opacity:0.9; margin-bottom:20px;" />
                <div style="font-size:1rem; color:#0F5C63; margin-bottom:6px;">
                    Seu assistente TR4CTION está pronto.
                </div>
                <div style="font-size:0.9rem;">
                    Envie uma mensagem para iniciar o atendimento 💬
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for msg in st.session_state.history:
            if msg["role"] == "user":
                st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='msg-agent'>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Entrada de texto
    st.markdown("<p style='margin-top:10px;font-weight:500;'> Enviar nova mensagem</p>", unsafe_allow_html=True)

    user_input = st.text_area("", placeholder="Digite sua pergunta, contexto ou resposta aqui...", key="user_input")

    if st.button("Enviar mensagem"):
        if user_input.strip():

            st.session_state.history.append({"role": "user", "content": user_input})
            response = agent.ask(step_key=step_key, history=st.session_state.history, user_input=user_input)

            st.session_state.history.append({"role": "assistant", "content": response})

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
# RODAPÉ
# =============================================
st.markdown(
    """
    <div style="margin-top:15px; text-align:right; color:#9CA3AF; font-size:0.8rem;">
        FCJ Venture Builder • TR4CTION Agent – protótipo acadêmico consultivo-operacional.
    </div>
    """,
    unsafe_allow_html=True,
)
