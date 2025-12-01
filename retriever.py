# retriever.py
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------------------
# LOAD MODEL (apenas 1 vez)
# -----------------------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# -----------------------------------------
# LOAD INDEX + TEXTS
# -----------------------------------------
def load_embeddings(index_path="embeddings/full_index.pkl",
                    texts_path="embeddings/full_texts.pkl"):
    with open(index_path, "rb") as f:
        index = pickle.load(f)
    with open(texts_path, "rb") as f:
        texts = pickle.load(f)
    return index, texts


EMBEDDING_INDEX, STORED_TEXTS = load_embeddings()


# -----------------------------------------
# BUSCA SEMÂNTICA
# -----------------------------------------
def search_memory(query: str, top_k: int = 5):
    """
    Retorna os textos mais semelhantes à pergunta do usuário.
    """
    # Converte pergunta em embedding
    q_emb = model.encode([query])[0]

    # Calcula similaridade por dot-product
    scores = np.dot(EMBEDDING_INDEX, q_emb)

    # Pega melhores trechos
    top_idx = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_idx:
        results.append(STORED_TEXTS[idx])

    return results
