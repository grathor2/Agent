"""Knowledge Retrieval Agent (RAG) - Searches large documents."""
from typing import Dict, Any
from rag.vector_store import VectorStore
from utils.logger import get_logger

logger = get_logger(__name__)

class KnowledgeRetrievalAgent:
    """Retrieves relevant knowledge using RAG."""
    
    def __init__(self):
        self.name = "knowledge_retrieval_agent"
        self.vector_store = VectorStore()
        logger.info("KnowledgeRetrievalAgent initialized")
    
    def retrieve(self, normalized_input: Dict[str, Any], k: int = 5) -> Dict[str, Any]:
        """Retrieve relevant knowledge."""
        logger.info("Knowledge retrieval started", 
                   input_id=normalized_input.get("id"),
                   k=k)
        
        query = normalized_input.get("content", "")
        
        try:
            # Retrieve from vector store
            documents = self.vector_store.similarity_search(query, k=k)
            
            # Format results
            retrieved_context = []
            for doc in documents:
                retrieved_context.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "type": doc.metadata.get("type", "unknown")
                })
            
            logger.info("Knowledge retrieval completed", 
                       results_count=len(retrieved_context))
            
            return {
                "agent": self.name,
                "status": "success",
                "output": {
                    "query": query,
                    "retrieved_documents": retrieved_context,
                    "count": len(retrieved_context)
                },
                "tool_calls": [{
                    "tool": "vector_store.similarity_search",
                    "input": {"query": query, "k": k},
                    "output": {"count": len(retrieved_context)}
                }],
                "execution_time": 0.3
            }
        except Exception as e:
            logger.error("Knowledge retrieval failed", error=str(e))
            return {
                "agent": self.name,
                "status": "error",
                "output": {"error": str(e), "retrieved_documents": []},
                "tool_calls": [],
                "execution_time": 0.1
            }
