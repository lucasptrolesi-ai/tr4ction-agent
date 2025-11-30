import streamlit as st
from agent_core import Tr4ctionAgent
from utils.data_manager import register_answer


# -----------------------------
# CONFIGURAÇÕES GERAIS
# -----------------------------
st.set_page_config(
    page_title="TR4CTION Agent",
    layout="wide",
    page_icon="🚀"
)

st.title("🚀 Agente TR4CTION – Q1")
st.markdown("### Assistente oficial da trilha de Marketing da FCJ Venture Builder")


# -----------------------------
# SIDEBAR – IDENTIFICAÇÃO
# -----------------------------
st.sidebar.header("Identificação do Founder")
startup_name = st.sidebar.text_input("Nome da Startup", placeholder="Ex: Trolesi Joias")
founder_name = st.sidebar.text_input("Seu nome", placeholder="Ex: Lucas Peixoto")


# -----------------------------
# FUNÇÃO PARA GERAR ID DO FOUNDER
# -----------------------------
def generate_founder_id(startup, founder):
    base = f"{startup}_{founder}".lower().replace(" ", "_")
    return base[:60]  # evita strings gigantes


if not (startup_name and founder_name):
    st.sidebar.warning("Preencha os dados acima para iniciar.")
    st.stop()

founder_id = generate_founder_id(startup_name, founder_name)
st.sidebar.success(f"ID gerado automaticamente: `{founder_id}`")


# -----------------------------
# LIMPA HISTÓRICO AO TROCAR FOUNDER
# -----------------------------
if "session_owner" not in st.session_state:
    st.session_state["session_owner"] = founder_id

if st.session_state["session_owner"] != founder_id:
    st.session_state["session_owner"] = founder_id
    st.session_state["history"] = []


# -----------------------------
# ETAPAS DO Q1
# -----------------------------
STEP_KEYS = {
    "Diagnóstico + CSD Canvas": "diagnostico",
    "ICP + SWOT": "icp_swot",
    "Persona + JTBD": "persona_jtbd",
}

etapa = st.selectbox("Escolha a etapa:", list(STEP_KEYS.keys()))
step_key = STEP_KEYS[etapa]

st.write(f"## 📌 Etapa atual: **{etapa}**")


# -----------------------------
# PIPELINE PREMIUM ANIMADO
# -----------------------------
def render_pipeline_animated(current_step):
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
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .step-block {
        display: flex;
        align-items: center;
        gap: 6px;
        min-width: 0;
    }
    .step-circle {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 2px solid #cccccc;
        box-sizing: border-box;
    }
    .step-label {
        font-size: 0.9rem;
        white-space: nowrap;
    }

    /* Estados */
    .done .step-circle {
        background: #16a34a;
        border-color: #16a34a;
    }
    .done .step-label {
        color: #16a34a;
        font-weight: 600;
    }

    .current .step-circle {
        background: #facc15;
        border-color: #eab308;
        box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.7);
        animation: pulse 1.4s infinite;
    }
    .current .step-label {
        color: #facc15;
        font-weight: 700;
    }

    .future .step-circle {
        background: transparent;
        border-color: #6b7280;
    }
    .future .step-label {
        color: #9ca3af;
    }

    .connector {
        flex: 1;
        height: 2px;
        background: linear-gradient(to right, #4b5563, #9ca3af);
        opacity: 0.7;
    }
    .connector.done {
        background: linear-gradient(to right, #16a34a, #4ade80);
        opacity: 0.9;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(250, 204, 21, 0.7);
        }
        70% {
            transform: scale(1.15);
            box-shadow: 0 0 0 10px rgba(250, 204, 21, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(250, 204, 21, 0);
        }
    }
    </style>
    <div class="pipeline-container">
      <div class="pipeline">
    """

    for i, step_key in enumerate(step_keys_order):
        if i < current_index:
            status_class = "done"
        elif i == current_index:
            status_class = "current"
        else:
            status_class = "future"

        html += f"""
        <div class="step-block {status_class}">
          <div class="step-circle"></div>
          <div class="step-label">{steps[step_key]}</div>
        </div>
        """

        if i < len(step_keys_order) - 1:
            connector_class = "done" if i < current_index else ""
            html += f'<div class="connector {connector_class}"></div>'

    html += """
      </div>
    </div>
    """

    st.markdown("### 📊 Pipeline de Progresso")
    st.markdown(html, unsafe_allow_html=True)


# Renderização do pipeline
render_pipeline_animated(step_key)


# -----------------------------
# AGENTE
# -----------------------------
agent = Tr4ctionAgent(startup_name)

if "history" not in st.session_state:
    st.session_state["history"] = []


# -----------------------------
# CAMPO DE MENSAGEM
# -----------------------------
st.markdown("### 💬 Conversa com o Agente TR4CTION")

user_input = st.text_area(
    "Digite sua mensagem:",
    placeholder="Ex: Minha startup vende X e atende Y...",
    height=120
)

enviar = st.button("Enviar 🚀")


# -----------------------------
# PROCESSAMENTO
# -----------------------------
if enviar:
    if not user_input.strip():
        st.warning("Digite algo antes de enviar.")
    else:
        st.session_state.history.append({"role": "user", "content": user_input})

        try:
            resposta = agent.ask(
                step_key=step_key,
                history=st.session_state.history,
                user_input=user_input,
                model="gpt-4.1-mini"
            )

            st.session_state.history.append({"role": "assistant", "content": resposta})

            register_answer(
                founder_id=founder_id,
                startup=startup_name,
                founder_name=founder_name,
                step=step_key,
                answer_text=resposta
            )

        except Exception as e:
            st.error("Erro ao consultar o agente.")
            st.exception(e)


# -----------------------------
# HISTÓRICO VISUAL
# -----------------------------
st.markdown("### 📝 Histórico da Conversa")

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="padding:10px;border-radius:8px;background:#e8e8e8;margin-bottom:8px;">
            <strong>👤 Você:</strong><br>{msg['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="padding:10px;border-radius:8px;background:#f0f9ff;margin-bottom:8px;">
            <strong>🤖 Agente:</strong><br>{msg['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# BOTÃO LIMPAR
# -----------------------------
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Limpar conversa"):
    st.session_state.history = []
    st.sidebar.success("Histórico apagado!")
