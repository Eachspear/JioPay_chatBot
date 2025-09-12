# faiss indexer (see canvas)
# backend/indexer.py
# Build FAISS index from embeddings and store mapping metadata.

import faiss
import numpy as np
import json, os

INDEX_PATH = 'data/faiss.index'
META_PATH = 'data/meta.json'


def build_faiss(embeddings, metadatas, dim=None):
    embeddings = np.array(embeddings).astype('float32')
    if dim is None:
        dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine via normalized embeddings -> IP
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadatas, f, ensure_ascii=False, indent=2)
    return INDEX_PATH, META_PATH


def load_index():
    if not os.path.exists(INDEX_PATH):
        return None, None
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    return index, meta


def search_index(index, query_emb, top_k=5):
    D, I = index.search(query_emb, top_k)
    return D, I