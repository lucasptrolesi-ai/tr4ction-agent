# TR4CTION Agent – FCJ Venture Builder

Agente de IA consultivo + operacional para apoiar founders da FCJ Venture Builder
na trilha de Marketing (Q1 da trilha TR4CTION).

O agente:

- Faz perguntas inteligentes antes de responder
- Usa o material oficial do TR4CTION como base (RAG)
- Guia o founder no preenchimento de:
  - Diagnóstico + CSD Canvas
  - ICP + SWOT
  - Persona + JTBD
- Salva respostas para análise posterior em um dashboard

---

## 🧱 Arquitetura (visão geral)

```mermaid
flowchart LR
    A[Founder\n(interface Streamlit)] --> B[app.py\n(Fluxo do chat)]
    B --> C[agent_core.py\n(Lógica do agente)]
    C --> D[prompts_q1.py\n(Prompts por etapa)]
    C --> E[retriever.py\n(RAG - Busca semântica)]
    E --> F[(embeddings/*.pkl)]
    C --> G[OpenAI API\n(modelo gpt-4.1-mini)]
    B --> H[utils/data_manager.py\n(Salva respostas)]
    H --> I[(data/answers.json)]
    J[dashboard.py\n(mentores)] --> H
