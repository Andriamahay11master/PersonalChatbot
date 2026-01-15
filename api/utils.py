# api/utils.py

import os
import yaml
import logging
import re
from typing import List, Dict, Any
from pathlib import Path

# ------------------------------------------------------------------
# Configuration handling
# ------------------------------------------------------------------

_CONFIG: Dict[str, Any] | None = None


def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    """
    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}
    except FileNotFoundError:
        logging.warning(
            f"Config file '{config_path}' not found. Using default configuration."
        )
        return {}
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return {}


def get_config() -> Dict[str, Any]:
    """
    Get cached configuration (singleton).
    """
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = load_config()
    return _CONFIG


# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

def setup_logging(level: str = "INFO") -> None:
    """
    Setup application-wide logging configuration.
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


# ------------------------------------------------------------------
# Text preprocessing
# ------------------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Clean and normalize raw text.
    """
    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text.strip())

    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    return text


def chunk_text(
    text: str,
    chunk_size: int = 300,
    overlap: int = 50,
) -> List[str]:
    """
    Split text into overlapping chunks (word-based).
    """
    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks: List[str] = []

    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        chunk = " ".join(chunk_words)
        if chunk:
            chunks.append(chunk)

    return chunks


# ------------------------------------------------------------------
# File handling
# ------------------------------------------------------------------

def save_uploaded_file(
    file_content: bytes,
    filename: str,
    upload_dir: str = "data/uploads",
) -> str:
    """
    Save uploaded file to disk and return the file path.
    """
    Path(upload_dir).mkdir(parents=True, exist_ok=True)

    safe_filename = os.path.basename(filename)
    file_path = os.path.join(upload_dir, safe_filename)

    with open(file_path, "wb") as f:
        f.write(file_content)

    return file_path


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a file.

    Currently supports plain text files.
    Can be extended to PDF, DOCX, etc.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        logging.warning(f"Could not decode file as UTF-8: {file_path}")
        return ""
    except Exception as e:
        logging.error(f"Failed to extract text from {file_path}: {e}")
        return ""


# ------------------------------------------------------------------
# Error handling helpers
# ------------------------------------------------------------------

def handle_api_error(
    error: Exception,
    status_code: int = 500,
) -> Dict[str, Any]:
    """
    Standardized error response structure.
    """
    logging.error(f"API error: {error}")
    return {
        "error": str(error),
        "status_code": status_code,
    }
