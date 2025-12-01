import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

DATA_PATH = Path("data/atr4ction/full")
INDEX_PATH = Path("embeddings/full_index.pkl")
TEXTS_PATH = Path("embeddings/full_texts.pkl")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def load_texts():
    texts = []
    for file in sorted(DATA_PATH.glob("*.txt")):
        content = file.read_text(encoding="utf-8").strip()
        if not content:
            print(f"⚠ Ignorado (vazio): {file.name}")
            continue
        texts.append(content)
        print(f"✔ Carregado: {file.name}")
    print(f"📚 Total carregado: {len(texts)} arquivos")
    return texts

if __name__ == "__main__":
    print("🚀 Lendo textos do TR4CTION...")
    texts = load_texts()

    print("⚡ Gerando embeddings localmente (zero custo)...")
    embeddings = model.encode(texts, convert_to_numpy=True)

    INDEX_PATH.parent.mkdir(exist_ok=True, parents=True)

    pickle.dump(embeddings, INDEX_PATH.open("wb"))
    pickle.dump(texts, TEXTS_PATH.open("wb"))

    print("\n🎉 Embeddings gerados com sucesso!")
    print(f"📁 Salvo em: {INDEX_PATH}")
    print(f"📁 Salvo em: {TEXTS_PATH}")
