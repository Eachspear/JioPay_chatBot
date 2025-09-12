# backend/build_index.py
import os, json, glob
from chunking import semantic_chunk   # you can swap for fixed_chunk, recursive_chunk, etc.
from embeddings import embed_texts
from indexer import build_faiss

DATA_DIR = "data/jiopay"
MODEL_NAME = "all-MiniLM-L6-v2"   # change to "e5-small" or "e5-large" if you want

def load_docs():
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    docs = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            try:
                docs.append(json.load(fh))
            except Exception as e:
                print(f"⚠️ Skipping {f}: {e}")
    print(f"Loaded {len(docs)} documents from {DATA_DIR}")
    return docs

def build_index():
    docs = load_docs()
    chunks = []

    for d in docs:
        if not d.get("text"):
            continue
        cs = semantic_chunk(d["text"])
        for c in cs:
            c["meta"] = {
                "url": d.get("url", ""),
                "title": d.get("title", ""),
                "text": c["text"],
            }
            chunks.append(c)

    print(f"Generated {len(chunks)} chunks")

    texts = [c["text"] for c in chunks]
    embs = embed_texts(texts, model_name=MODEL_NAME)
    build_faiss(embs, chunks)
    print("✅ FAISS index built and saved!")

if __name__ == "__main__":
    build_index()
