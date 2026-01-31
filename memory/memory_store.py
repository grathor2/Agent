"""Memory store for Working, Episodic, and Semantic memory."""
import sqlite3
import json
from typing import Dict, List, Any, Optional
from enum import Enum
from config import MEMORY_DB_PATH, MAX_WORKING_MEMORY_SIZE
from utils.logger import get_logger

logger = get_logger(__name__)

class MemoryType(Enum):
    """Memory type enumeration."""
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"

class MemoryStore:
    """Manages persistent memory storage."""
    
    def __init__(self):
        self.db_path = MEMORY_DB_PATH
        self._initialize_db()
        logger.info("MemoryStore initialized", db_path=str(self.db_path))
    
    def _initialize_db(self):
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Working memory table (short-lived, task-level)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS working_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                UNIQUE(session_id, key)
            )
        """)
        
        # Episodic memory table (past incidents, conversations, outcomes)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                conversation_id TEXT,
                event_type TEXT NOT NULL,
                content TEXT NOT NULL,
                outcome TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Semantic memory table (documents, FAQs, runbooks)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_working_session ON working_memory(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_episodic_incident ON episodic_memory(incident_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_episodic_conversation ON episodic_memory(conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_semantic_key ON semantic_memory(key)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_semantic_category ON semantic_memory(category)")
        
        conn.commit()
        conn.close()
    
    def write_working_memory(self, session_id: str, key: str, value: Any, ttl: Optional[int] = None):
        """Write to working memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        expires_at = None
        if ttl:
            from datetime import timedelta
            expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO working_memory 
            (session_id, key, value, expires_at)
            VALUES (?, ?, ?, ?)
        """, (session_id, key, json.dumps(value), expires_at))
        
        conn.commit()
        conn.close()
        logger.info("Working memory written", session_id=session_id, key=key)
    
    def read_working_memory(self, session_id: str, key: Optional[str] = None) -> Dict[str, Any]:
        """Read from working memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clean expired entries
        cursor.execute("DELETE FROM working_memory WHERE expires_at < datetime('now')")
        
        if key:
            cursor.execute("""
                SELECT key, value FROM working_memory 
                WHERE session_id = ? AND key = ?
            """, (session_id, key))
        else:
            cursor.execute("""
                SELECT key, value FROM working_memory 
                WHERE session_id = ?
            """, (session_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        memory = {}
        for row in results:
            memory[row[0]] = json.loads(row[1])
        
        logger.info("Working memory read", session_id=session_id, 
                   key=key, count=len(memory))
        return memory
    
    def clear_working_memory(self, session_id: str):
        """Clear working memory for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM working_memory WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
        logger.info("Working memory cleared", session_id=session_id)
    
    def write_episodic_memory(
        self, 
        event_type: str, 
        content: str,
        incident_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        outcome: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> int:
        """Write to episodic memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO episodic_memory 
            (incident_id, conversation_id, event_type, content, outcome, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            incident_id,
            conversation_id,
            event_type,
            content,
            outcome,
            json.dumps(metadata) if metadata else None
        ))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        logger.info("Episodic memory written", 
                   memory_id=memory_id, event_type=event_type)
        return memory_id
    
    def read_episodic_memory(
        self,
        incident_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Read from episodic memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM episodic_memory WHERE 1=1"
        params = []
        
        if incident_id:
            query += " AND incident_id = ?"
            params.append(incident_id)
        if conversation_id:
            query += " AND conversation_id = ?"
            params.append(conversation_id)
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in rows:
            result = dict(zip(columns, row))
            if result.get('metadata'):
                result['metadata'] = json.loads(result['metadata'])
            results.append(result)
        
        logger.info("Episodic memory read", count=len(results))
        return results
    
    def write_semantic_memory(
        self,
        key: str,
        content: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ):
        """Write to semantic memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO semantic_memory 
            (key, content, category, tags, metadata, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            key,
            content,
            category,
            json.dumps(tags) if tags else None,
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
        logger.info("Semantic memory written", key=key, category=category)
    
    def read_semantic_memory(
        self,
        key: Optional[str] = None,
        category: Optional[str] = None,
        search_term: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Read from semantic memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if key:
            cursor.execute("SELECT * FROM semantic_memory WHERE key = ?", (key,))
        elif category:
            cursor.execute("""
                SELECT * FROM semantic_memory 
                WHERE category = ? 
                ORDER BY access_count DESC, updated_at DESC 
                LIMIT ?
            """, (category, limit))
        elif search_term:
            cursor.execute("""
                SELECT * FROM semantic_memory 
                WHERE content LIKE ? OR key LIKE ?
                ORDER BY access_count DESC 
                LIMIT ?
            """, (f"%{search_term}%", f"%{search_term}%", limit))
        else:
            cursor.execute("""
                SELECT * FROM semantic_memory 
                ORDER BY access_count DESC, updated_at DESC 
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Update access count
        for row in rows:
            row_dict = dict(zip(columns, row))
            cursor.execute("""
                UPDATE semantic_memory 
                SET access_count = access_count + 1 
                WHERE id = ?
            """, (row_dict['id'],))
        
        conn.commit()
        conn.close()
        
        results = []
        for row in rows:
            result = dict(zip(columns, row))
            if result.get('tags'):
                result['tags'] = json.loads(result['tags'])
            if result.get('metadata'):
                result['metadata'] = json.loads(result['metadata'])
            results.append(result)
        
        logger.info("Semantic memory read", count=len(results))
        return results
    
    def delete_memory(self, memory_type: MemoryType, memory_id: int) -> bool:
        """Delete a memory entry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        table_map = {
            MemoryType.WORKING: "working_memory",
            MemoryType.EPISODIC: "episodic_memory",
            MemoryType.SEMANTIC: "semantic_memory"
        }
        
        table = table_map.get(memory_type)
        if not table:
            return False
        
        cursor.execute(f"DELETE FROM {table} WHERE id = ?", (memory_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        logger.info("Memory deleted", memory_type=memory_type.value, 
                   memory_id=memory_id, deleted=deleted)
        return deleted
    
    def get_all_memories(self, memory_type: MemoryType, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all memories of a type (for UI display)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        table_map = {
            MemoryType.WORKING: "working_memory",
            MemoryType.EPISODIC: "episodic_memory",
            MemoryType.SEMANTIC: "semantic_memory"
        }
        
        table = table_map.get(memory_type)
        if not table:
            return []
        
        cursor.execute(f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        results = []
        for row in rows:
            result = dict(zip(columns, row))
            if result.get('metadata'):
                try:
                    result['metadata'] = json.loads(result['metadata'])
                except:
                    pass
            if result.get('tags'):
                try:
                    result['tags'] = json.loads(result['tags'])
                except:
                    pass
            results.append(result)
        
        conn.close()
        return results
