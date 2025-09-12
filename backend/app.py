# backend/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from retriever import retrieve
from generator import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="JioPay RAG Chatbot",
    description="Retrieval-Augmented Generation chatbot for JioPay support",
    version="1.0.0"
)

# ✅ Enable CORS so frontend (React/Vite) can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ChatReq(BaseModel):
    query: str
    top_k: int = 5
    embed_model: str = "all-MiniLM-L6-v2"

# Response schema
class ChatResp(BaseModel):
    answer: str
    retrieved: List[dict]


@app.post("/chat", response_model=ChatResp)
async def chat(req: ChatReq):
    """
    Main chat endpoint:
    - Retrieves relevant chunks
    - Generates an answer grounded in sources
    """
    try:
        results = retrieve(req.query, model_name=req.embed_model, top_k=req.top_k)
        answer = generate_answer(req.query, results)
        return {"answer": answer, "retrieved": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "✅ JioPay RAG backend is running!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
