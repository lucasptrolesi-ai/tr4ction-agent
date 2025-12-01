import time
import traceback
import openai
from openai import OpenAI


class Tr4ctionAgent:
    """
    Agente oficial TR4CTION Q1 ― FCJ Venture Builder
    Responsável por gerar respostas com base no histórico e na etapa escolhida.
    """

    def __init__(self, startup_name: str):
        self.startup_name = startup_name
        self.client = OpenAI()

        # Modelo padrão (estável e rápido)
        self.model = "gpt-4o-mini"

    # ======================================================================
    #  FUNÇÃO PRINCIPAL (ASK) COM RETRY E TRATAMENTO ROBUSTO
    # ======================================================================
    def ask(self, step_key: str, history: list, user_input: str) -> str:
        """
        step_key: etapa atual (diagnóstico, ICP, SWOT, Persona…)
        history: histórico completo (lista de dicts)
        user_input: mensagem atual do usuário
        """

        # ---------------------------
        # Montar histórico para o LLM
        # ---------------------------
        messages = [
            {
                "role": "system",
                "content": (
                    f"Você é o TR4CTION Agent da FCJ Venture Builder. "
                    f"Ajude o founder da startup '{self.startup_name}' "
                    f"na etapa '{step_key}'."
                ),
            }
        ]

        # histórico completo
        for msg in history:
            messages.append(
                {
                    "role": msg["role"],
                    "content": msg["content"],
                }
            )

        # mensagem atual do usuário
        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # ---------------------------
        # Retry automático (RateLimit)
        # ---------------------------
        max_retries = 5
        base_delay = 2

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,
                )

                return response.choices[0].message["content"]

            except openai.RateLimitError:
                wait = base_delay * (attempt + 1)
                time.sleep(wait)

            except Exception as e:
                traceback.print_exc()
                return f"⚠️ Ocorreu um erro inesperado: {str(e)}"

        # Se chegou aqui, falhou todas as tentativas
        return (
            "⚠️ A API da OpenAI atingiu o limite de requisições no momento.\n"
            "Tente novamente em alguns instantes."
        )
