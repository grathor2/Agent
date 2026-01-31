"""Configuration management for the collaborative agent system."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = DATA_DIR / "vectorstore"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"
MEMORY_DB_PATH = DATA_DIR / "memory.db"
LOGS_DIR = BASE_DIR / "logs"
DOCUMENTS_DIR = DATA_DIR / "documents"
IMAGES_DIR = DATA_DIR / "images"
GENERATED_DIR = DATA_DIR / "generated"

# Create directories
for dir_path in [DATA_DIR, VECTOR_STORE_DIR, CHROMA_DB_DIR, LOGS_DIR, 
                 DOCUMENTS_DIR, IMAGES_DIR, GENERATED_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")

# RAG Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "8000"))

# Memory Configuration
MEMORY_TYPES = ["working", "episodic", "semantic"]
MAX_WORKING_MEMORY_SIZE = 5000
MAX_EPISODIC_MEMORY_ENTRIES = 1000
MAX_SEMANTIC_MEMORY_ENTRIES = 10000

# Guardrails Configuration
MIN_CONFIDENCE_THRESHOLD = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.7"))
CONTENT_FILTER_CATEGORIES = ["violence", "self_harm", "sexual", "hate", "jailbreak"]

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "agent_system.log"

# Supported file types
SUPPORTED_FILE_TYPES = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}
