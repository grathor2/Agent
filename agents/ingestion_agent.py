"""Ingestion Agent - Normalizes incoming tickets and queries."""
from typing import Dict, Any, Union
from datetime import datetime
import uuid
from utils.logger import get_logger

logger = get_logger(__name__)

class IngestionAgent:
    """Normalizes and structures incoming tickets/queries."""
    
    def __init__(self):
        self.name = "ingestion_agent"
        logger.info("IngestionAgent initialized")
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """Process and normalize incoming data."""
        logger.info("Ingestion started", input_type=type(input_data).__name__)
        
        # Handle string input
        if isinstance(input_data, str):
            input_data = {"content": input_data, "type": "query"}
        
        # Ensure it's a dict
        if not isinstance(input_data, dict):
            input_data = {"content": str(input_data), "type": "unknown"}
        
        # Normalize input
        normalized = {
            "id": input_data.get("id") or str(uuid.uuid4()),
            "session_id": input_data.get("session_id") or str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "raw_input": input_data,
            "type": self._detect_type(input_data),
            "content": self._extract_content(input_data),
            "metadata": self._extract_metadata(input_data),
            "source": input_data.get("source", "unknown")
        }
        
        logger.info("Ingestion completed", 
                   normalized_id=normalized["id"],
                   type=normalized["type"])
        
        return {
            "agent": self.name,
            "status": "success",
            "output": normalized,
            "tool_calls": [],
            "execution_time": 0.1
        }
    
    def _detect_type(self, input_data: Dict[str, Any]) -> str:
        """Detect input type."""
        if isinstance(input_data, dict):
            if "ticket" in input_data or "incident" in input_data:
                return "ticket"
            elif "query" in input_data or "question" in input_data:
                return "query"
            elif "chat" in input_data or "message" in input_data:
                return "chat"
        elif isinstance(input_data, str):
            return "query"
        return "unknown"
    
    def _extract_content(self, input_data: Dict[str, Any]) -> str:
        """Extract content from input."""
        if isinstance(input_data, str):
            return input_data
        
        content_fields = ["content", "message", "query", "question", "description", "ticket", "incident"]
        for field in content_fields:
            if field in input_data:
                return str(input_data[field])
        
        return str(input_data)
    
    def _extract_metadata(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from input."""
        metadata = {}
        metadata_fields = ["priority", "urgency", "category", "user_id", 
                          "timestamp", "source", "tags"]
        for field in metadata_fields:
            if field in input_data:
                metadata[field] = input_data[field]
        return metadata
