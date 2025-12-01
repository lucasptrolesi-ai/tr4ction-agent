# agent_core.py
"""
Cérebro do TR4CTION Agent.

- Monta mensagens (prompt + RAG + histórico + entrada)
- Chama o modelo da OpenAI
"""

from typing import Dict, List, Optional

from openai import OpenAI

from config import DEFAULT_OPENAI_MODEL, OPENAI_API_KEY
from prompts_q1 import STEP_PROMPTS
from retriever import search_memory

client = OpenAI(api_key=OPENAI_API_KEY)


class Tr4ctionAgent:
    """
    Agente TR4CTION com RAG (busca semântica).
    Usa o conteúdo oficial das aulas como memória.
    """

    def __init__(self, startup_name: str):
        self.startup_name = startup_name

    # --------------------------------------------------------
    # MONTA MENSAGENS (Prompt + Memória + Histórico + Usuário)
    # --------------------------------------------------------
    def build_messages(
        self,
        step_key: str,
        history: List[Dict[str, str]],
        user_input: str,
    ) -> List[Dict[str, str]]:
        base_prompt = STEP_PROMPTS.get(step_key)

        if not base_prompt:
            base_prompt = (
                "Você é um agente da FCJ. Responda com clareza e profundidade, "
                "guiando o founder a preencher os templates do Q1."
            )

        # 🔍 Busca semântica no material oficial do TR4CTION
        try:
            memory_chunks = search_memory(user_input, top_k=5)
        except FileNotFoundError:
            memory_chunks = []

        if memory_chunks:
            memory_text = "\n\n".join(memory_chunks)
        else:
            memory_text = (
                "Nenhum trecho específico do material foi recuperado para esta pergunta. "
                "Responda com base nas boas práticas da trilha TR4CTION, "
                "mantendo profundidade e linguagem simples."
            )

        memory_block = (
            "### CONTEXTO OFICIAL DO TR4CTION (RAG)\n"
            "Use as informações abaixo como referência quando forem relevantes.\n\n"
            f"{memory_text}\n\n"
        )

        # Mensagem inicial (system)
        messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    base_prompt
                    + f"\n\nStartup atual: {self.startup_name}\n\n"
                    + memory_block
                ),
            }
        ]

        # Histórico da conversa
        for msg in history:
            # espera-se {"role": "user"/"assistant", "content": "..."}
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Pergunta atual
        if user_input:
            messages.append({"role": "user", "content": user_input})

        return messages

    # --------------------------------------------------------
    # CHAMA O MODELO (com RAG)
    # --------------------------------------------------------
    def ask(
        self,
        step_key: str,
        history: List[Dict[str, str]],
        user_input: str,
        model: Optional[str] = None,
    ) -> str:
        messages = self.build_messages(step_key, history, user_input)

        model_name = model or DEFAULT_OPENAI_MODEL

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
        )

        return response.choices[0].message.content
