#----------------------------------FastAPI app----------------------------------#
# api/main.py 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import router as api_router

app = FastAPI(title="RetrievalQA Chatbot")

# Simple CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"ok": True, "message": "Retrieval-Augmented QA API"}
