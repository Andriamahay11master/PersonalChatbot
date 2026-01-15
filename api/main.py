# api/main.py
# ---------------------------------- FastAPI application entry ---------------------------------- #

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .endpoints import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown logic.
    """
    # ------------------- Startup -------------------
    # Place for:
    # - loading models
    # - warming up vector stores
    # - initializing external services
    print("🚀 API starting up...")
    yield
    # ------------------- Shutdown ------------------
    print("🛑 API shutting down...")


app = FastAPI(
    title="Retrieval-Augmented QA Chatbot API",
    version="0.1.0",
    description="Personal RAG-based chatbot backend built with FastAPI",
    lifespan=lifespan,
)

# ------------------------------------------------------------------
# CORS (allow frontend access)
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
app.include_router(api_router, prefix="/api")

# ------------------------------------------------------------------
# Root endpoint
# ------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "ok": True,
        "message": "Retrieval-Augmented QA API is running"
    }
