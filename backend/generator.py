# backend/generator.py
# Generate answers grounded in retrieved chunks using Flan-T5 small (free, on HF).

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "google/flan-t5-small"  # small and free; suitable for CPU experiments

_tokenizer = None
_model = None


def load_model():
    """Load the tokenizer and model once (lazy load)."""
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return _tokenizer, _model


def build_prompt(query, retrieved, max_context_chars=3000):
    """
    Construct a prompt for Flan-T5 using retrieved chunks.
    retrieved: list of {'score','meta':{'text','url','title'}}
    """
    context_pieces = []
    added = 0
    for r in retrieved:
        t = r["meta"].get("text", "")
        snippet = t[:500]  # keep snippet manageable
        context_pieces.append(f"Source: {r['meta'].get('url','')}\n{snippet}")
        added += len(snippet)
        if added > max_context_chars:
            break
    context = "\n\n---\n\n".join(context_pieces)

    prompt = (
        "You are a helpful customer support assistant for JioPay. "
        "Answer the user's question using ONLY the provided sources. "
        "If the answer is not in the sources, say: "
        "'I don't know, please check JioPay official support.'\n\n"
        f"User question: {query}\n\n"
        f"Sources:\n{context}\n\n"
        "Answer:"
    )
    return prompt


def generate_answer(query, retrieved, max_new_tokens=200):
    """Generate an answer from the model using the built prompt."""
    tokenizer, model = load_model()
    prompt = build_prompt(query, retrieved)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_beams=3,
            early_stopping=True,
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
