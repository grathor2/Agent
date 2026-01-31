"""Memory Agent - Manages episodic and semantic memory."""
from typing import Dict, Any, List, Optional
from memory.memory_store import MemoryStore, MemoryType
from utils.logger import get_logger

logger = get_logger(__name__)

class MemoryAgent:
    """Manages memory operations."""
    
    def __init__(self):
        self.name = "memory_agent"
        self.memory_store = MemoryStore()
        logger.info("MemoryAgent initialized")
    
    def read_memory(
        self, 
        normalized_input: Dict[str, Any],
        memory_types: List[str] = ["episodic", "semantic"]
    ) -> Dict[str, Any]:
        """Read from memory."""
        logger.info("Memory read started", 
                   input_id=normalized_input.get("id"),
                   types=memory_types)
        
        session_id = normalized_input.get("session_id", "")
        content = normalized_input.get("content", "")
        
        results = {}
        tool_calls = []
        
        try:
            # Read working memory
            if "working" in memory_types:
                working = self.memory_store.read_working_memory(session_id)
                results["working"] = working
                tool_calls.append({
                    "tool": "memory_store.read_working_memory",
                    "input": {"session_id": session_id},
                    "output": {"count": len(working)}
                })
            
            # Read episodic memory (search for similar incidents)
            if "episodic" in memory_types:
                episodic = self.memory_store.read_episodic_memory(
                    conversation_id=session_id,
                    limit=5
                )
                results["episodic"] = episodic
                tool_calls.append({
                    "tool": "memory_store.read_episodic_memory",
                    "input": {"conversation_id": session_id},
                    "output": {"count": len(episodic)}
                })
            
            # Read semantic memory (search for relevant knowledge)
            if "semantic" in memory_types:
                semantic = self.memory_store.read_semantic_memory(
                    search_term=content[:50],
                    limit=5
                )
                results["semantic"] = semantic
                tool_calls.append({
                    "tool": "memory_store.read_semantic_memory",
                    "input": {"search_term": content[:50]},
                    "output": {"count": len(semantic)}
                })
            
            logger.info("Memory read completed", 
                       working_count=len(results.get("working", {})),
                       episodic_count=len(results.get("episodic", [])),
                       semantic_count=len(results.get("semantic", [])))
            
            return {
                "agent": self.name,
                "status": "success",
                "output": results,
                "tool_calls": tool_calls,
                "execution_time": 0.2
            }
        except Exception as e:
            logger.error("Memory read failed", error=str(e))
            return {
                "agent": self.name,
                "status": "error",
                "output": {"error": str(e)},
                "tool_calls": [],
                "execution_time": 0.1
            }
    
    def write_memory(
        self,
        normalized_input: Dict[str, Any],
        memory_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Write to memory."""
        logger.info("Memory write started", 
                   input_id=normalized_input.get("id"),
                   memory_type=memory_type)
        
        session_id = normalized_input.get("session_id", "")
        
        try:
            if memory_type == "working":
                for key, value in data.items():
                    self.memory_store.write_working_memory(session_id, key, value)
            elif memory_type == "episodic":
                self.memory_store.write_episodic_memory(
                    event_type=data.get("event_type", "unknown"),
                    content=data.get("content", ""),
                    conversation_id=session_id,
                    outcome=data.get("outcome"),
                    metadata=data.get("metadata")
                )
            elif memory_type == "semantic":
                self.memory_store.write_semantic_memory(
                    key=data.get("key", ""),
                    content=data.get("content", ""),
                    category=data.get("category"),
                    tags=data.get("tags"),
                    metadata=data.get("metadata")
                )
            
            logger.info("Memory write completed", memory_type=memory_type)
            
            return {
                "agent": self.name,
                "status": "success",
                "output": {"written": True, "memory_type": memory_type},
                "tool_calls": [{
                    "tool": f"memory_store.write_{memory_type}_memory",
                    "input": data,
                    "output": {"success": True}
                }],
                "execution_time": 0.15
            }
        except Exception as e:
            logger.error("Memory write failed", error=str(e))
            return {
                "agent": self.name,
                "status": "error",
                "output": {"error": str(e)},
                "tool_calls": [],
                "execution_time": 0.1
            }
