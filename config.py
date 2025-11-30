# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY não encontrado. Crie um arquivo .env com a linha:\n"
        "OPENAI_API_KEY=suas_chave_aqui"
    )
