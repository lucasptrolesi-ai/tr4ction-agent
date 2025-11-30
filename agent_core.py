# agent_core.py
from typing import List, Dict
from openai import OpenAI
from config import OPENAI_API_KEY
from prompts_q1 import STEP_PROMPTS   # ✅ Corrigido aqui

client = OpenAI(api_key=OPENAI_API_KEY)


class Tr4ctionAgent:
    """
    Agente TR4CTION responsável por conduzir o founder
    nas etapas do Q1, de forma consultiva e operacional.
    """

    def __init__(self, startup_name: str):
        self.startup_name = startup_name

    def build_messages(
        self,
        step_key: str,
        history: List[Dict[str, str]],
        user_input: str,
    ) -> List[Dict[str, str]]:
        """
        Monta o histórico de mensagens no formato esperado pela API.
        """
        system_prompt = STEP_PROMPTS.get(step_key)

        if not system_prompt:
            system_prompt = (
                "Você é um agente de marketing da FCJ. Ajude o usuário com orientações claras."
            )

        messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": system_prompt
                + f"\n\nStartup atual: {self.startup_name}\n",
            }
        ]

        # histórico vindo do Streamlit (user/assistant)
        for item in history:
            messages.append({"role": item["role"], "content": item["content"]})

        # última mensagem do usuário
        if user_input:
            messages.append({"role": "user", "content": user_input})

        return messages

    def ask(
        self,
        step_key: str,
        history: List[Dict[str, str]],
        user_input: str,
        model: str = "gpt-4.1-mini",
    ) -> str:
        """
        Envia a conversa para o modelo da OpenAI e retorna a resposta.
        """
        messages = self.build_messages(step_key, history, user_input)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
        )

        return response.choices[0].message.content
