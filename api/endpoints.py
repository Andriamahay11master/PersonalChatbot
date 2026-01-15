# api/endpoints.py
# -------------------- routes for chat, upload-file, and health endpoints -------------------- #

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from starlette.concurrency import run_in_threadpool

from .schemas import (
    ChatRequest,
    ChatResponse,
    UploadResponse,
    HealthResponse,
)
from .qa_pipeline import QAPipeline

router = APIRouter()

# ------------------------------------------------------------------
# Initialize QA pipeline ONCE (safe if pipeline is stateless)
# ------------------------------------------------------------------
_qa_pipeline: QAPipeline | None = None


def get_qa_pipeline() -> QAPipeline:
    """
    Dependency injector for QA pipeline.
    Ensures a single shared instance.
    """
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = QAPipeline()
    return _qa_pipeline


# ------------------------------------------------------------------
# Chat endpoint
# ------------------------------------------------------------------
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest,
    qa: QAPipeline = Depends(get_qa_pipeline),
):
    """
    Chat endpoint for Q&A with document retrieval (RAG).
    """
    try:
        # Run blocking QA logic in a thread pool
        answer, sources = await run_in_threadpool(
            qa.answer,
            req.prompt,
            req.session_id,
        )

        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=req.session_id,
        )

    except ValueError as e:
        # Client-side input issues
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        # Never leak internal errors
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


# ------------------------------------------------------------------
# Upload documents endpoint
# ------------------------------------------------------------------
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = (".pdf", ".txt", ".md")


@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    qa: QAPipeline = Depends(get_qa_pipeline),
):
    """
    Upload documents for ingestion into the vector store.
    """
    if not files:
        raise HTTPException(
            status_code=400,
            detail="No files provided",
        )

    uploaded_files: List[str] = []

    try:
        for file in files:
            filename = file.filename.lower()

            if not filename.endswith(ALLOWED_EXTENSIONS):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file.filename}",
                )

            contents = await file.read()

            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename} exceeds the 5MB size limit",
                )

            uploaded_files.append(file.filename)

            # --------------------------------------------------
            # TODO (next step):
            # 1. Extract text from file
            # 2. Chunk text
            # 3. Embed chunks
            # 4. Store in vector database
            #
            # Example:
            # text = extract_text(contents, file.filename)
            # qa.ingest_documents([text])
            # --------------------------------------------------

        return UploadResponse(
            count=len(uploaded_files),
            file_ids=uploaded_files,
            message=f"Successfully uploaded {len(uploaded_files)} file(s)",
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to process uploaded files",
        )


# ------------------------------------------------------------------
# Health check endpoint
# ------------------------------------------------------------------
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    """
    return HealthResponse(status="healthy")
