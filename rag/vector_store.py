"""Vector store for RAG with ChromaDB."""
from typing import List, Optional
try:
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OpenAIEmbeddings
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document
from config import CHROMA_DB_DIR, EMBEDDING_MODEL, OPENAI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

class VectorStore:
    """Manages vector store for RAG retrieval."""
    
    def __init__(self):
        if OpenAIEmbeddings is None:
            raise ImportError("OpenAIEmbeddings not available. Install langchain-openai.")
        if Chroma is None:
            raise ImportError("Chroma not available. Install chromadb and langchain-community.")
        
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        self.vectorstore: Optional[Chroma] = None
        self._initialize_store()
        logger.info("VectorStore initialized")
    
    def _initialize_store(self):
        """Initialize or load existing vector store."""
        try:
            # Try to import chromadb
            try:
                import chromadb
            except ImportError:
                # Check if pydantic-settings is the issue
                try:
                    import pydantic_settings
                    import chromadb
                except Exception as e:
                    logger.warning("ChromaDB import failed, will use fallback", error=str(e))
                    self.vectorstore = None
                    return
            
            self.vectorstore = Chroma(
                persist_directory=str(CHROMA_DB_DIR),
                embedding_function=self.embeddings
            )
            logger.info("Vector store loaded", path=str(CHROMA_DB_DIR))
        except Exception as e:
            logger.warning("Could not initialize vector store", error=str(e))
            # Create empty store that will work but won't have data
            try:
                self.vectorstore = Chroma(
                    persist_directory=str(CHROMA_DB_DIR),
                    embedding_function=self.embeddings
                )
            except Exception as e2:
                logger.warning("Vector store initialization failed, using fallback mode", error=str(e2))
                self.vectorstore = None
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to vector store."""
        if not self.vectorstore:
            self._initialize_store()
        
        try:
            ids = self.vectorstore.add_documents(documents)
            self.vectorstore.persist()
            logger.info("Documents added to vector store", count=len(documents))
            return ids
        except Exception as e:
            logger.error("Failed to add documents", error=str(e))
            return []
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 5
    ) -> List[Document]:
        """Search for similar documents."""
        if not self.vectorstore:
            self._initialize_store()
            if not self.vectorstore:
                logger.warning("Vector store unavailable, returning empty results")
                return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info("Similarity search completed", 
                       query=query[:50], 
                       results_count=len(results))
            return results
        except Exception as e:
            logger.error("Similarity search failed", query=query, error=str(e))
            return []
    
