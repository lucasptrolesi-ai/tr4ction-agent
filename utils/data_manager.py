"""
Camada simples de persistência dos dados de resposta.

Hoje grava em arquivo JSONL local (um JSON por linha) apenas para protótipo.
Em produção, a ideia é trocar por um banco (Postgres, BigQuery, etc.).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


BASE_PATH = Path("data")
BASE_PATH.mkdir(exist_ok=True)

ANSWER_FILE = BASE_PATH / "answers.jsonl"


def register_answer(
    founder_id: str,
    startup: str,
    founder_name: str,
    step: str,
    answer_text: str,
) -> None:
    """
    Registra uma resposta do agente em formato de linha JSON.

    Esse formato é ótimo para:
    - Ler em lote depois (pandas lê JSONL fácil)
    - Fazer análises de progresso dos founders
    """
    record: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat(),
        "founder_id": founder_id,
        "startup": startup,
        "founder_name": founder_name,
        "step": step,
        "answer": answer_text,
    }

    with ANSWER_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_answers() -> List[Dict[str, Any]]:
    """
    Carrega todas as respostas já registradas.
    """
    if not ANSWER_FILE.exists():
        return []

    rows: List[Dict[str, Any]] = []
    with ANSWER_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # Em caso de linha corrompida, apenas ignora.
                continue
    return rows
