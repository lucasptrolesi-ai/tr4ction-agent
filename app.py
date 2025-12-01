# app.py
import streamlit as st

from agent_core import Tr4ctionAgent
from prompts_q1 import LABEL_TO_STEP_KEY, STEP_CONFIG, STEP_ORDER
from utils.data_manager import register_answer


# ============================================
#  CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="TR4CTION Agent",
    layout="wide",
    page_icon="🚀",
)

st.title("🚀 Agente TR4CTION – Q1")
st.markdown("### Assistente oficial da trilha de Marketing da FCJ Venture Builder")


# ============================================
# SIDEBAR – IDENTIFICAÇÃO
# ============================================
st.sidebar.header("Identificação do Founder")

startup_name = st.sidebar.text_input(
    "Nome da Startup", placeholder="Ex: Trolesi Joias"
)
founder_name = st.sidebar.text_input("Seu nome", placeholder="Ex: Lucas Peixoto")


def generate_founder_id(startup: str, founder: str) -> str:
    """Gera um ID simples e legível para o founder."""
    base = f"{startup}_{founder}".lower().replace(" ", "_")
    return base[:60]


if not (startup_name and founder_name):
    st.sidebar.warning("Preencha os dados acima para iniciar o atendimento.")
    st.stop()

founder_id = generate_founder_id(startup_name, founder_name)
st.sidebar.success(f"ID gerado automaticamente: `{founder_id}`")

# Reset de sessão ao trocar founder
if "session_owner" not in st.session_state:
    st.session_state.session_owner = founder_id

if st.session_state.session_owner != founder_id:
    st.session_state.session_owner = founder_id
    st.session_state.history = []


# ============================================
# ETAPAS DO Q1
# ============================================
# Usa a ordem definida em STEP_ORDER
step_labels = [STEP_CONFIG[key]["label"] for key in STEP_ORDER]

etapa_label = st.selectbox("Escolha a etapa:", step_labels)
step_key = LABEL_TO_STEP_KEY[etapa_label]

st.write(f"## 📌 Etapa atual: **{etapa_label}**")


# ============================================
# PIPELINE PREMIUM ANIMADO
# ============================================
def render_pipeline_animated(current_step: str):
    steps = {
        "diagnostico": "Diagnóstico",
        "icp_swot": "ICP + SWOT",
        "persona_jtbd": "Persona + JTBD",
    }

    step_keys_order = list(steps.keys())
    current_index = step_keys_order.index(current_step)

    html = """
    <style>
    .pipeline-container {
        margin-top: 10px;
        margin-bottom: 25px;
    }
    .pipeline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
    }
    .step-block {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .step-circle {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 2px solid #cccccc;
    }
    .step-label {
        font-size: 0.9rem;
        white-space: nowrap;
    }
    .done .step-circle {
        background: #16a34a;
        border-color: #16a34a;
    }
    .current .step-circle {
        background: #facc15;
        border-color: #eab308;
        animation: pulse 1.4s infinite;
    }
    .future .step-circle {
        background: transparent;
        border-color: #6b7280;
    }
    .connector {
        flex: 1;
        height: 2px;
        background: #6b7280;
        opacity: 0.4;
    }
    .connector.done {
        background: #16a34a;
        opacity: 0.9;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    </style>
    <div class="pipeline-container">
      <div class="pipeline">
    """

    for i, s_key in enumerate(step_keys_order):
        if i < current_index:
            status_class = "done"
        elif i == current_index:
            status_class = "current"
        else:
            status_class = "future"

        html += f"""
        <div class="step-block {status_class}">
          <div class="step-circle"></div>
          <div class="step-label">{steps[s_key]}</div>
        </div>
        """

        if i < len(step_keys_order) - 1:
            connector_class = "done" if i < current_index else ""
            html += f'<div class="connector {connector_class}"></div>'

    html += "</div></div>"

    st.markdown("### 📊 Pipeline de Progresso")
    st.markdown(html, unsafe_allow_html=True)


render_pipeline_animated(step_key)


# ============================================
# AGENTE
# ============================================
agent = Tr4ctionAgent(startup_name)

if "history" not in st.session_state:
    st.session_state.history = []

MAX_HISTORY = 20  # limite para não explodir a sessão


# ============================================
# CAIXA DE TEXTO DO FOUNDER
# ============================================
st.markdown("### 💬 Conversa com o Agente TR4CTION")

user_input = st.text_area(
    "Digite sua mensagem:",
    placeholder="Ex: Minha startup vende X e resolve Y...",
    height=120,
)

btn = st.button("Enviar 🚀")


# ============================================
# PROCESSAMENTO DO AGENTE
# ============================================
if btn:
    if not user_input.strip():
        st.warning("Digite algo antes de enviar.")
    else:
        st.session_state.history.append({"role": "user", "content": user_input})

        # Limita histórico
        if len(st.session_state.history) > MAX_HISTORY:
            st.session_state.history = st.session_state.history[-MAX_HISTORY:]

        try:
            response = agent.ask(
                step_key=step_key,
                history=st.session_state.history,
                user_input=user_input,
                model="gpt-4.1-mini",
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

        except Exception as e:
            st.error("Erro ao consultar o agente. Verifique logs e configuração.")
            st.exception(e)


# ============================================
# HISTÓRICO DA CONVERSA (CHAT VISUAL)
# ============================================
st.markdown("### 📝 Histórico da Conversa")

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="padding:12px;border-radius:8px;background:#e7e7e7;margin-bottom:10px;">
            <strong>👤 Você:</strong><br>{msg['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="padding:12px;border-radius:8px;background:#eef7ff;margin-bottom:10px;">
            <strong>🤖 Agente:</strong><br>{msg['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================
# BOTÃO LIMPAR
# ============================================
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Limpar conversa"):
    st.session_state.history = []
    st.sidebar.success("Histórico apagado!")
