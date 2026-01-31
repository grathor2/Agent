"""Setup script to index documents in the knowledge base."""
import os
from pathlib import Path
from rag import DocumentProcessor, VectorStore
from config import GENERATED_DIR, DOCUMENTS_DIR
from utils.logger import get_logger

logger = get_logger(__name__)

def index_documents(directory: Path):
    """Index all documents in a directory."""
    processor = DocumentProcessor()
    vector_store = VectorStore()
    
    supported_extensions = [".pdf", ".docx", ".txt", ".pptx", ".png", ".jpg", ".jpeg"]
    files = []
    
    for ext in supported_extensions:
        files.extend(list(directory.glob(f"*{ext}")))
    
    logger.info("Found files to index", count=len(files), directory=str(directory))
    
    total_documents = 0
    for file_path in files:
        try:
            logger.info("Processing file", file_path=str(file_path))
            documents = processor.process_file(str(file_path))
            if documents:
                chunked = processor.chunk_documents(documents)
                vector_store.add_documents(chunked)
                total_documents += len(chunked)
                logger.info("File indexed", file_path=str(file_path), chunks=len(chunked))
        except Exception as e:
            logger.error("Failed to index file", file_path=str(file_path), error=str(e))
    
    logger.info("Indexing completed", total_documents=total_documents)
    return total_documents

if __name__ == "__main__":
    print("Setting up knowledge base...")
    
    # Index generated test data
    if GENERATED_DIR.exists():
        print(f"Indexing test data from {GENERATED_DIR}...")
        index_documents(GENERATED_DIR)
    
    # Index any documents in documents directory
    if DOCUMENTS_DIR.exists():
        print(f"Indexing documents from {DOCUMENTS_DIR}...")
        index_documents(DOCUMENTS_DIR)
    
    print("✅ Knowledge base setup complete!")
