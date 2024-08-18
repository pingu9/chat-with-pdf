from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.rag import RAGPipeline
from app.models import ModelManager

router = APIRouter()

# rag_pipeline = RAGPipeline(documents)
model_manager = ModelManager()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        # answer = rag_pipeline.retrieve_and_generate(request.question)
        answer = model_manager.generate_answer(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

