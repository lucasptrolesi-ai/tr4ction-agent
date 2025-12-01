# config.py
"""
Configurações centrais do projeto TR4CTION Agent.

- Carrega variáveis de ambiente (.env)
- Expõe a OPENAI_API_KEY validada
- Define modelo padrão da OpenAI
"""

import os

from dotenv import load_dotenv

# Carrega variáveis do arquivo .env, se existir
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY não encontrado.\n\n"
        "Crie um arquivo `.env` na raiz do projeto com a linha:\n"
        "OPENAI_API_KEY=sua_chave_aqui"
    )

# Modelo padrão para o agente (pode mudar depois se quiser)
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
