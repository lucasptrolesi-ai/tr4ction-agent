# embeddings_builder_local.py
"""
Script para gerar embeddings locais a partir dos textos oficiais
do TR4CTION (arquivos .txt em data/atr4ction/full).

Uso:
    python embeddings_builder_local.py
"""

import pickle
from pathlib import Path

from sentence_transformers import SentenceTransformer

DATA_PATH = Path("data/atr4ction/full")
INDEX_PATH = Path("embeddings/full_index.pkl")
TEXTS_PATH = Path("embeddings/full_texts.pkl")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_texts():
    """Carrega todos os arquivos .txt da pasta data/atr4ction/full."""
    texts = []
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Pasta {DATA_PATH} não encontrada.\n"
            "Crie data/atr4ction/full e coloque os materiais do TR4CTION em .txt."
        )

    for file in sorted(DATA_PATH.glob("*.txt")):
        content = file.read_text(encoding="utf-8").strip()
        if not content:
            print(f"⚠ Ignorado (vazio): {file.name}")
            continue
        texts.append(content)
        print(f"✔ Carregado: {file.name}")

    print(f"📚 Total carregado: {len(texts)} arquivos")
    if not texts:
        raise ValueError("Nenhum texto válido encontrado em data/atr4ction/full")
    return texts


def main():
    print("🚀 Lendo textos do TR4CTION...")
    texts = load_texts()

    print("⚡ Gerando embeddings localmente (zero custo)...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, convert_to_numpy=True)

    INDEX_PATH.parent.mkdir(exist_ok=True, parents=True)

    with INDEX_PATH.open("wb") as f:
        pickle.dump(embeddings, f)

    with TEXTS_PATH.open("wb") as f:
        pickle.dump(texts, f)

    print("\n🎉 Embeddings gerados com sucesso!")
    print(f"📁 Salvo em: {INDEX_PATH}")
    print(f"📁 Salvo em: {TEXTS_PATH}")


if __name__ == "__main__":
    main()
