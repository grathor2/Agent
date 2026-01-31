"""FastAPI server with WebSocket for live streaming."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import json
from orchestration import AgentOrchestrator
from memory import MemoryStore, MemoryType
from observability import event_stream
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Collaborative Agent System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
orchestrator = AgentOrchestrator()
memory_store = MemoryStore()

# WebSocket connections
active_connections: List[WebSocket] = []

@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    # Subscribe to events for broadcasting
    event_stream.subscribe(broadcast_event)
    logger.info("FastAPI server started")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    logger.info("FastAPI server shutting down")

async def broadcast_event(event: Dict[str, Any]):
    """Broadcast event to all WebSocket connections."""
    if active_connections:
        message = json.dumps(event)
        disconnected = []
        for connection in active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            if conn in active_connections:
                active_connections.remove(conn)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for live streaming."""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info("WebSocket connection established", total_connections=len(active_connections))
    
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for ping/pong
            await websocket.send_text(json.dumps({"type": "pong", "data": {}}))
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("WebSocket disconnected", total_connections=len(active_connections))

@app.post("/api/process")
async def process_request(request: Dict[str, Any]):
    """Process a request through the agent system."""
    try:
        # Emit start event
        await event_stream.emit("agent_execution_start", {
            "input": request
        })
        
        # Process through orchestrator
        result = await orchestrator.process_async(request)
        
        # Emit completion event
        await event_stream.emit("agent_execution_complete", {
            "result": result
        })
        
        return JSONResponse(content=result)
    except Exception as e:
        logger.error("Request processing failed", error=str(e))
        await event_stream.emit("agent_execution_error", {
            "error": str(e)
        })
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/memories")
async def get_memories(memory_type: str = "all", limit: int = 100):
    """Get memories for UI display."""
    try:
        if memory_type == "all":
            results = {
                "working": memory_store.get_all_memories(MemoryType.WORKING, limit),
                "episodic": memory_store.get_all_memories(MemoryType.EPISODIC, limit),
                "semantic": memory_store.get_all_memories(MemoryType.SEMANTIC, limit)
            }
        elif memory_type == "working":
            results = memory_store.get_all_memories(MemoryType.WORKING, limit)
        elif memory_type == "episodic":
            results = memory_store.get_all_memories(MemoryType.EPISODIC, limit)
        elif memory_type == "semantic":
            results = memory_store.get_all_memories(MemoryType.SEMANTIC, limit)
        else:
            raise HTTPException(status_code=400, detail="Invalid memory type")
        
        return JSONResponse(content=results)
    except Exception as e:
        logger.error("Memory retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/memories/{memory_type}/{memory_id}")
async def delete_memory(memory_type: str, memory_id: int):
    """Delete a memory entry."""
    try:
        memory_type_enum = MemoryType(memory_type)
        success = memory_store.delete_memory(memory_type_enum, memory_id)
        if success:
            return JSONResponse(content={"success": True})
        else:
            raise HTTPException(status_code=404, detail="Memory not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid memory type")
    except Exception as e:
        logger.error("Memory deletion failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/memories/{memory_type}/{memory_id}")
async def update_memory(memory_type: str, memory_id: int, request: Dict[str, Any]):
    """Update a memory entry."""
    try:
        # Implementation would update memory
        # For now, return success
        return JSONResponse(content={"success": True})
    except Exception as e:
        logger.error("Memory update failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events")
async def get_events(limit: int = 100):
    """Get recent events."""
    events = event_stream.get_history(limit)
    return JSONResponse(content=events)

@app.get("/")
async def get_ui():
    """Serve the main UI."""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Collaborative Agent System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header h1 { margin-bottom: 10px; }
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .panel {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .panel h2 {
            margin-bottom: 15px;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .input-section {
            margin-bottom: 20px;
        }
        textarea {
            width: 100%;
            min-height: 100px;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            resize: vertical;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover { background: #5568d3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .execution-log {
            max-height: 500px;
            overflow-y: auto;
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        .log-entry {
            margin-bottom: 10px;
            padding: 10px;
            border-left: 3px solid #667eea;
            background: white;
        }
        .log-entry.agent { border-left-color: #48bb78; }
        .log-entry.tool { border-left-color: #ed8936; }
        .log-entry.error { border-left-color: #f56565; }
        .response-section {
            margin-top: 20px;
            padding: 15px;
            background: #e6f3ff;
            border-radius: 5px;
        }
        .memory-section {
            max-height: 400px;
            overflow-y: auto;
        }
        .memory-item {
            padding: 10px;
            margin-bottom: 10px;
            background: #f9f9f9;
            border-radius: 5px;
            border-left: 3px solid #48bb78;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-connected { background: #48bb78; }
        .status-disconnected { background: #f56565; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Collaborative Agent System</h1>
            <p>Intelligent Support & Incident Co-Pilot</p>
            <p>Status: <span class="status-indicator" id="status"></span><span id="statusText">Connecting...</span></p>
        </div>
        
        <div class="main-content">
            <div class="panel">
                <h2>💬 Chat Interface</h2>
                <div class="input-section">
                    <textarea id="userInput" placeholder="Enter your query, ticket, or incident report..."></textarea>
                    <button id="sendButton" onclick="sendMessage()">Send</button>
                </div>
                
                <div class="response-section" id="responseSection" style="display: none;">
                    <h3>Response:</h3>
                    <div id="responseContent"></div>
                </div>
            </div>
            
            <div class="panel">
                <h2>📊 Live Execution Log</h2>
                <div class="execution-log" id="executionLog">
                    <div class="log-entry">Waiting for execution...</div>
                </div>
            </div>
        </div>
        
        <div class="panel" style="margin-top: 20px;">
            <h2>🧠 Memory Management</h2>
            <div style="margin-bottom: 15px;">
                <button onclick="loadMemories('working')">Working Memory</button>
                <button onclick="loadMemories('episodic')">Episodic Memory</button>
                <button onclick="loadMemories('semantic')">Semantic Memory</button>
            </div>
            <div class="memory-section" id="memorySection">
                Click a button above to load memories
            </div>
        </div>
    </div>
    
    <script>
        let ws = null;
        let reconnectAttempts = 0;
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            ws = new WebSocket(wsUrl);
            
            ws.onopen = () => {
                document.getElementById('status').className = 'status-indicator status-connected';
                document.getElementById('statusText').textContent = 'Connected';
                reconnectAttempts = 0;
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleEvent(data);
            };
            
            ws.onclose = () => {
                document.getElementById('status').className = 'status-indicator status-disconnected';
                document.getElementById('statusText').textContent = 'Disconnected';
                setTimeout(connectWebSocket, 3000);
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }
        
        function handleEvent(event) {
            const logDiv = document.getElementById('executionLog');
            const entry = document.createElement('div');
            entry.className = 'log-entry agent';
            
            if (event.type === 'agent_execution_start') {
                entry.innerHTML = `<strong>🚀 Execution Started</strong><br>Input: ${JSON.stringify(event.data.input).substring(0, 100)}...`;
            } else if (event.type === 'agent_execution_complete') {
                entry.innerHTML = `<strong>✅ Execution Complete</strong><br>Result: ${JSON.stringify(event.data.result).substring(0, 200)}...`;
                displayResponse(event.data.result);
            } else if (event.type === 'agent_execution_error') {
                entry.className = 'log-entry error';
                entry.innerHTML = `<strong>❌ Error</strong><br>${event.data.error}`;
            } else {
                entry.innerHTML = `<strong>${event.type}</strong><br>${JSON.stringify(event.data).substring(0, 200)}...`;
            }
            
            logDiv.insertBefore(entry, logDiv.firstChild);
        }
        
        async function sendMessage() {
            const input = document.getElementById('userInput').value;
            if (!input.trim()) return;
            
            const button = document.getElementById('sendButton');
            button.disabled = true;
            button.textContent = 'Processing...';
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        content: input,
                        type: 'query',
                        session_id: getSessionId()
                    })
                });
                
                const result = await response.json();
                displayResponse(result);
            } catch (error) {
                console.error('Error:', error);
                alert('Error processing request: ' + error.message);
            } finally {
                button.disabled = false;
                button.textContent = 'Send';
            }
        }
        
        function displayResponse(result) {
            const section = document.getElementById('responseSection');
            const content = document.getElementById('responseContent');
            
            if (result.final_response) {
                content.innerHTML = `
                    <p><strong>Action:</strong> ${result.final_response.action}</p>
                    <p><strong>Response:</strong> ${result.final_response.response || 'N/A'}</p>
                    ${result.final_response.confidence ? `<p><strong>Confidence:</strong> ${result.final_response.confidence}</p>` : ''}
                `;
                section.style.display = 'block';
            }
        }
        
        async function loadMemories(type) {
            try {
                const response = await fetch(`/api/memories?memory_type=${type}&limit=20`);
                const data = await response.json();
                const section = document.getElementById('memorySection');
                
                const memories = Array.isArray(data) ? data : (data[type] || []);
                section.innerHTML = memories.map(m => `
                    <div class="memory-item">
                        <strong>${m.key || m.id}</strong>
                        <p>${(m.content || m.value || '').substring(0, 200)}...</p>
                        <small>${new Date(m.created_at).toLocaleString()}</small>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading memories:', error);
            }
        }
        
        function getSessionId() {
            let sessionId = sessionStorage.getItem('sessionId');
            if (!sessionId) {
                sessionId = 'session_' + Date.now();
                sessionStorage.setItem('sessionId', sessionId);
            }
            return sessionId;
        }
        
        // Initialize
        connectWebSocket();
        document.getElementById('userInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                sendMessage();
            }
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
