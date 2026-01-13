import os
import yaml
import logging
import re
from typing import List, Dict, Any
from pathlib import Path

# Load configuration from settings.yaml
def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.warning(f"Config file {config_path} not found, using defaults")
        return {}
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

# Setup logging
def setup_logging(level: str = "INFO"):
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Text preprocessing utilities
def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

# File handling utilities
def save_uploaded_file(file_content: bytes, filename: str, upload_dir: str = "data/uploads") -> str:
    """Save uploaded file to disk and return the path."""
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    return file_path

def extract_text_from_file(file_path: str) -> str:
    """Extract text from various file formats (placeholder for PDF, DOCX, etc.)."""
    # For now, assume plain text files
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Handle binary files or other encodings
        logging.warning(f"Could not decode {file_path} as text")
        return ""

# Error handling
def handle_api_error(error: Exception, status_code: int = 500) -> Dict[str, Any]:
    """Standardize error responses."""
    logging.error(f"API Error: {error}")
    return {
        "error": str(error),
        "status_code": status_code
    }

# Configuration singleton
_config = None
def get_config() -> Dict[str, Any]:
    """Get cached configuration."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
