#--------------------routes for chat, upload-file, and other endpoints--------------------#
# api/endpoints.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from .schemas import ChatRequest, ChatResponse, UploadResponse, ErrorResponse, HealthResponse
from .qa_pipeline import QAPipeline

router = APIRouter()

# Initialize QA pipeline
qa = QAPipeline()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Chat endpoint for Q&A with document retrieval."""
    try:
        answer, sources = qa.answer(req.prompt)
        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=req.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload documents for ingestion into the vector store."""
    try:
        uploaded_files = []
        for file in files:
            contents = await file.read()
            # TODO: Save file and process with utils
            # For now, just acknowledge
            uploaded_files.append(file.filename)

        # TODO: Extract text, create embeddings, update vector store
        # qa.ingest_documents(extracted_texts)

        return UploadResponse(
            count=len(files),
            file_ids=uploaded_files,
            message=f"Successfully uploaded {len(files)} files"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")

