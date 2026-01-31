"""Event streaming for real-time observability."""
import asyncio
from typing import Dict, Any, List, Callable
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

class EventStream:
    """Manages real-time event streaming for observability."""
    
    def __init__(self):
        self.subscribers: List[Callable] = []
        self.event_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        logger.info("EventStream initialized")
    
    def subscribe(self, callback: Callable):
        """Subscribe to events."""
        self.subscribers.append(callback)
        logger.info("New subscriber added", total_subscribers=len(self.subscribers))
    
    def unsubscribe(self, callback: Callable):
        """Unsubscribe from events."""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
            logger.info("Subscriber removed", total_subscribers=len(self.subscribers))
    
    async def emit(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to all subscribers."""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history = self.event_history[-self.max_history:]
        
        # Notify subscribers
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                logger.error("Event callback failed", error=str(e))
        
        logger.debug("Event emitted", event_type=event_type)
    
    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get event history."""
        return self.event_history[-limit:]
    
    def clear_history(self):
        """Clear event history."""
        self.event_history = []
        logger.info("Event history cleared")

# Global event stream instance
event_stream = EventStream()
