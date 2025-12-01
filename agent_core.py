# agent_core.py
from typing import List, Dict
from openai import OpenAI
from config import OPENAI_API_KEY
from prompts_q1 import STEP_PROMPTS
from retriever import search_memory


client = OpenAI(api_key=OPENAI_API_KEY)


class Tr4ctionAgent:
    """
    Agente TR4CTION com RAG (busca semântica).
    Agora ele usa o conteúdo oficial das aulas como memória.
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
            base_prompt = "Você é um agente da FCJ. Responda com clareza e profundidade."

        # 🔍 Busca semântica no TR4CTION
        memory_chunks = search_memory(user_input, top_k=5)
        memory_text = "\n\n".join(memory_chunks)

        memory_block = (
            "### CONTEXTO OFICIAL DO TR4CTION (RAG)\n"
            "Use APENAS informações abaixo caso sejam relevantes.\n"
            "Não invente nada que não esteja no material TR4CTION.\n\n"
            f"{memory_text}\n\n"
        )

        # Mensagem inicial
        messages = [
            {
                "role": "system",
                "content": (
                    base_prompt
                    + f"\n\nStartup atual: {self.startup_name}\n\n"
                    + memory_block
                ),
            }
        ]

        # Histórico
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Pergunta atual
        if user_input:
            messages.append({"role": "user", "content": user_input})

        return messages

    # --------------------------------------------------------
    # CHAMA O MODELO (agora com RAG)
    # --------------------------------------------------------
    def ask(
        self,
        step_key: str,
        history: List[Dict[str, str]],
        user_input: str,
        model: str = "gpt-4.1-mini",
    ) -> str:

        messages = self.build_messages(step_key, history, user_input)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
        )

        return response.choices[0].message.content
