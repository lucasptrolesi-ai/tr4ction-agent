# utils/data_manager.py
"""
Persistência simples das respostas do TR4CTION Agent.

- Salva respostas em data/answers.json
- Permite carregar para o dashboard
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path("data")
ANSWERS_PATH = DATA_DIR / "answers.json"


def load_answers() -> List[Dict]:
    """Carrega todas as respostas já registradas."""
    if not ANSWERS_PATH.exists():
        return []

    try:
        with ANSWERS_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except json.JSONDecodeError:
        # Em caso de arquivo corrompido
        return []


def register_answer(
    founder_id: str,
    startup: str,
    founder_name: str,
    step: str,
    answer_text: str,
) -> None:
    """Registra uma nova resposta no arquivo answers.json."""
    DATA_DIR.mkdir(exist_ok=True, parents=True)

    answers = load_answers()

    answers.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "founder_id": founder_id,
            "startup": startup,
            "founder_name": founder_name,
            "step": step,
            "answer": answer_text,
        }
    )

    with ANSWERS_PATH.open("w", encoding="utf-8") as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)
