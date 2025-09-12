# embeddings wrappers (see canvas)
# backend/embeddings.py
# wrappers to compute embeddings using sentence-transformers and E5 models.

from sentence_transformers import SentenceTransformer
import numpy as np

MODELS = {
    'all-MiniLM-L6-v2': 'sentence-transformers/all-MiniLM-L6-v2',
    'e5-small': 'intfloat/e5-small',
    'e5-large': 'intfloat/e5-large'  # larger model, slower
}

_cache = {}

def get_model(name='all-MiniLM-L6-v2'):
    if name in _cache:
        return _cache[name]
    m = SentenceTransformer(MODELS[name])
    _cache[name]=m
    return m


def embed_texts(texts, model_name='all-MiniLM-L6-v2', batch_size=32):
    model = get_model(model_name)
    embs = model.encode(texts, batch_size=batch_size, show_progress_bar=True)
    # normalize
    embs = np.array(embs, dtype='float32')
    norms = np.linalg.norm(embs, axis=1, keepdims=True) + 1e-10
    embs = embs / norms
    return embs