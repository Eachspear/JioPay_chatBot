# retriever (see canvas)
from embeddings import embed_texts
from indexer import load_index, search_index
import numpy as np


def retrieve(query, model_name='all-MiniLM-L6-v2', top_k=5):
    idx, meta = load_index()
    if idx is None:
        raise RuntimeError('Index not found. Build it first.')
    q_emb = embed_texts([query], model_name=model_name)
    D, I = search_index(idx, q_emb.astype('float32'), top_k=top_k)
    results=[]
    for score, i in zip(D[0], I[0]):
        if i < 0:
            continue
        m = meta[i]
        results.append({'score': float(score), 'meta': m})
    return results