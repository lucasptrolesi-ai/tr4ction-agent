# utils/knowledge_base.py

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Dict, Tuple

import numpy as np
from openai import OpenAI

from config import OPENAI_API_KEY

# Cliente OpenAI (mesmo do agente)
client = OpenAI(api_key=OPENAI_API_KEY)

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "atr4ction"
INDEX_PATH = BASE_DIR / "data" / "atr4ction_index.json"

# Modelo de embedding
EMBEDDING_MODEL = "text-embedding-3-small"

# Tamanho dos pedaços (em caracteres) – simples e robusto
CHUNK_SIZE = 900
CHUNK_OVERLAP = 200


# -----------------------------
# Utilidades básicas
# -----------------------------
def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Divide o texto em pedaços com sobreposição simples, baseado em caracteres.
    Não é perfeito, mas é suficientemente bom para o MVP do curso.
    """
    text = text.strip().replace("\r", "")
    chunks: List[str] = []

    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # volta um pouco pra manter contexto

    return chunks


def _embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Gera embeddings usando o modelo da OpenAI.
    """
    if not texts:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    return [item.embedding for item in response.data]


# -----------------------------
# Construção / atualização do índice
# -----------------------------
def build_index_from_files() -> Dict:
    """
    Lê todos os .txt dentro de data/atr4ction/<step_key>/,
    corta em chunks e gera os embeddings.
    Retorna um dicionário pronto para ser salvo em JSON.
    """
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Pasta {DATA_DIR} não encontrada. "
            f"Crie data/atr4ction/diagnostico, icp_swot, persona_jtbd e coloque os .txt lá."
        )

    rows: List[Dict] = []

    for step_dir in DATA_DIR.iterdir():
        if not step_dir.is_dir():
            continue

        step_key = step_dir.name  # ex: "diagnostico", "icp_swot", "persona_jtbd"

        for txt_path in step_dir.glob("*.txt"):
            try:
                text = txt_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                # tenta fallback de encoding
                text = txt_path.read_text(errors="ignore")

            chunks = _chunk_text(text)

            for idx, chunk in enumerate(chunks):
                rows.append(
                    {
                        "id": f"{step_key}__{txt_path.stem}__{idx}",
                        "step": step_key,
                        "source": str(txt_path.relative_to(BASE_DIR)),
                        "chunk_index": idx,
                        "text": chunk,
                    }
                )

    if not rows:
        raise ValueError(
            "Nenhum texto encontrado nas pastas de dados. "
            "Confira se você colocou arquivos .txt em data/atr4ction/<etapa>/."
        )

    # Gera embeddings em lotes pra evitar requisição gigante
    all_embeddings: List[List[float]] = []
    batch_size = 32

    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        texts = [r["text"] for r in batch]
        embeddings = _embed_texts(texts)
        all_embeddings.extend(embeddings)

    # Conferência
    if len(all_embeddings) != len(rows):
        raise RuntimeError("Número de embeddings diferente do número de chunks.")

    # Anexa os embeddings em cada row
    for r, emb in zip(rows, all_embeddings):
        r["embedding"] = emb

    index = {
        "model": EMBEDDING_MODEL,
        "rows": rows,
    }

    # Garante pasta data/
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    INDEX_PATH.write_text(json.dumps(index), encoding="utf-8")

    return index


def load_index() -> Dict:
    """
    Carrega o índice do disco. Se não existir, dispara erro amigável.
    """
    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            f"Índice {INDEX_PATH} não encontrado.\n"
            f"Rode antes: python -m utils.knowledge_base rebuild"
        )

    raw = INDEX_PATH.read_text(encoding="utf-8")
    return json.loads(raw)


def get_index_arrays() -> Tuple[List[Dict], np.ndarray]:
    """
    Retorna (rows, embeddings_array) preparados para cálculo de similaridade.
    """
    index = load_index()
    rows: List[Dict] = index["rows"]
    embeddings = np.array([r["embedding"] for r in rows], dtype="float32")
    return rows, embeddings


# -----------------------------
# Busca de contexto
# -----------------------------
def retrieve_context(step_key: str, question: str, top_k: int = 5) -> List[str]:
    """
    Dado o step atual (diagnostico, icp_swot, persona_jtbd) e a pergunta do founder,
    retorna os trechos mais relevantes dos materiais oficiais.
    """
    rows, embeddings = get_index_arrays()

    # Filtra por step (e opcionalmente por "global" se você criar depois)
    mask_indices = [
        i for i, r in enumerate(rows) if r.get("step") in (step_key, "global")
    ]

    if not mask_indices:
        # fallback: usa tudo
        mask_indices = list(range(len(rows)))

    sub_embs = embeddings[mask_indices]

    # embedding da pergunta
    query_emb = np.array(_embed_texts([question])[0], dtype="float32")

    # similaridade coseno
    dot = sub_embs @ query_emb
    norms = np.linalg.norm(sub_embs, axis=1) * np.linalg.norm(query_emb)
    sims = dot / (norms + 1e-8)

    # top_k índices ordenados (decrescente)
    top_idx = np.argsort(-sims)[:top_k]

    selected_chunks: List[str] = []
    for idx in top_idx:
        row = rows[mask_indices[idx]]
        selected_chunks.append(row["text"])

    return selected_chunks


# -----------------------------
# CLI simples
# -----------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2 and sys.argv[1] == "rebuild":
        print("🔄 Recriando índice de conhecimento a partir dos arquivos .txt...")
        idx = build_index_from_files()
        print(f"✅ Índice salvo em: {INDEX_PATH} (chunks: {len(idx['rows'])})")
    else:
        print("Uso:")
        print("  python -m utils.knowledge_base rebuild")
        print("para reconstruir o índice a partir dos arquivos em data/atr4ction.")
