# retriever.py
"""
Módulo de recuperação semântica (RAG) para o TR4CTION Agent.

- Carrega embeddings já gerados em disco
- Usa SentenceTransformer para gerar embeddings da pergunta
- Faz busca por similaridade (cosseno)
"""

import pickle
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache()
def _load_model() -> SentenceTransformer:
    """Carrega o modelo de embeddings apenas uma vez (cache em memória)."""
    return SentenceTransformer(_MODEL_NAME)


def load_embeddings(
    index_path: str = "embeddings/full_index.pkl",
    texts_path: str = "embeddings/full_texts.pkl",
) -> Tuple[np.ndarray, List[str]]:
    """
    Carrega o índice de embeddings e os textos originais.

    Levanta FileNotFoundError se os arquivos não existirem.
    """
    index_p = Path(index_path)
    texts_p = Path(texts_path)

    if not index_p.exists() or not texts_p.exists():
        raise FileNotFoundError(
            "Arquivos de embeddings não encontrados.\n\n"
            "Rode o comando abaixo ANTES de usar o agente:\n"
            "    python embeddings_builder_local.py\n"
        )

    with index_p.open("rb") as f:
        index = pickle.load(f)

    with texts_p.open("rb") as f:
        texts = pickle.load(f)

    return index, texts


@lru_cache()
def get_embeddings() -> Tuple[np.ndarray, List[str]]:
    """Wrapper com cache para não recarregar arquivos toda hora."""
    return load_embeddings()


def search_memory(query: str, top_k: int = 5) -> List[str]:
    """
    Retorna os textos mais semelhantes à pergunta do usuário.

    - Usa similaridade de cosseno
    - top_k controla quantos trechos retornam
    """
    query = query.strip()
    if not query:
        return []

    model = _load_model()
    index, texts = get_embeddings()

    # Embedding da pergunta
    q_emb = model.encode([query], convert_to_numpy=True)[0]

    # Similaridade de cosseno
    index_norms = np.linalg.norm(index, axis=1)
    q_norm = np.linalg.norm(q_emb)

    denom = index_norms * q_norm
    denom[denom == 0] = 1e-9  # evita divisão por zero

    scores = np.dot(index, q_emb) / denom

    # Top-K
    top_k = min(top_k, len(scores))
    top_idx = np.argsort(scores)[::-1][:top_k]

    return [texts[i] for i in top_idx]
