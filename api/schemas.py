from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Chat-related schemas
class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User's question or prompt")
    history: Optional[List[ChatMessage]] = Field(default=None, description="Previous conversation history")
    session_id: Optional[str] = Field(default=None, description="Session identifier for conversation continuity")
    max_sources: Optional[int] = Field(default=3, ge=1, le=10, description="Maximum number of sources to retrieve")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Generated answer to the user's prompt")
    sources: List[str] = Field(default_factory=list, description="List of source documents used")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Confidence score of the answer")
    session_id: Optional[str] = Field(default=None, description="Session identifier")

# Upload-related schemas
class UploadResponse(BaseModel):
    ok: bool = Field(default=True, description="Success status")
    count: int = Field(..., description="Number of files uploaded")
    file_ids: Optional[List[str]] = Field(default=None, description="IDs of uploaded files")
    message: Optional[str] = Field(default=None, description="Additional message")

# Document-related schemas
class DocumentInfo(BaseModel):
    id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    content_type: Optional[str] = Field(default=None, description="MIME type of the document")
    size: Optional[int] = Field(default=None, description="File size in bytes")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, description="Upload timestamp")

class DocumentListResponse(BaseModel):
    documents: List[DocumentInfo] = Field(..., description="List of documents")
    total: int = Field(..., description="Total number of documents")

# Error schemas
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")

# Health check schema
class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    version: Optional[str] = Field(default=None, description="API version")
    uptime: Optional[str] = Field(default=None, description="Service uptime")

# Configuration schema (for settings endpoint if needed)
class ConfigResponse(BaseModel):
    embedding_model: Optional[str] = None
    vector_store_type: Optional[str] = None
    max_upload_size: Optional[str] = None
    api_host: Optional[str] = None
    api_port: Optional[int] = None
