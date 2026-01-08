#--------------------routes for chat, upload-file, and other endpoints--------------------#
# api/endpoints.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    history: Optional[List[dict]] = None  # optional chat history for context

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []

# Placeholder for real pipeline integration
@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # TODO: wire to your QA pipeline: retrieve docs, run LM, format response
    return ChatResponse(answer="This is a stub. Implement QA pipeline.", sources=[])
