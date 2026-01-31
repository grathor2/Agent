# Collaborative Agent System - Intelligent Support & Incident Co-Pilot

A production-grade multi-agent system built with LangGraph for intelligent support ticket processing, incident management, and knowledge retrieval.

## 🎯 Features

### Core Capabilities
- **8 Specialized Agents**: Ingestion, Planner, Intent Classification, Knowledge Retrieval, Memory, Reasoning, Response Synthesis, Guardrails
- **RAG System**: Multi-format document support (PDF, Word, TXT, PPTX, Images with OCR)
- **Memory Management**: Working, Episodic, and Semantic memory with persistence
- **Guardrails & Safety**: Content filtering, confidence thresholds, escalation policies
- **Live Observability**: Real-time WebSocket streaming of agent execution
- **Context Management**: Automatic summarization and pruning for long conversations

### Execution Models
- **Serial Execution**: When dependencies exist
- **Parallel Execution**: Independent agents run simultaneously
- **Asynchronous Execution**: Memory updates and observability

## 📁 Project Structure

```
artifacts/
├── agents/              # All 8 agents (separate files)
│   ├── ingestion_agent.py
│   ├── planner_agent.py
│   ├── intent_classification_agent.py
│   ├── knowledge_retrieval_agent.py
│   ├── memory_agent.py
│   ├── reasoning_agent.py
│   ├── response_synthesis_agent.py
│   └── guardrails_agent.py
├── rag/                 # RAG system
│   ├── document_processor.py
│   └── vector_store.py
├── memory/              # Memory management
│   └── memory_store.py
├── orchestration/       # LangGraph orchestration
│   ├── agent_graph.py
│   └── context_manager.py
├── guardrails/          # Safety and policy
├── observability/       # Event streaming
│   └── event_stream.py
├── ui/                  # Web UI with live streaming
│   └── main.py
├── tests/               # Test suite
│   ├── test_agents.py
│   └── generate_test_data.py
├── data/                # Data directories
│   ├── documents/
│   ├── images/
│   └── generated/
├── config.py           # Configuration
├── requirements.txt    # Dependencies
└── README.md
```

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9+
- OpenAI API key
- Tesseract OCR (for image processing)

### 2. Installation

```bash
# Clone or navigate to the project directory
cd artifacts

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# macOS: brew install tesseract
# Ubuntu: sudo apt-get install tesseract-ocr
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

### 3. Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

### 4. Generate Test Data

```bash
python tests/generate_test_data.py
```

This generates 100+ test files (30 PDFs, 30 DOCX, 25 TXT, 15 PPTX) with 5-6 pages each.

### 5. Index Knowledge Base

```bash
python setup_knowledge_base.py
```

This indexes all documents in the `data/generated/` and `data/documents/` directories.

### 6. Run the System

```bash
# Start the FastAPI server
python -m ui.main

# Or using uvicorn directly
uvicorn ui.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Access the UI

Open your browser and navigate to:
```
http://localhost:8000
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/test_agents.py -v
```

## 📊 Architecture

### Agent Flow

```
Incoming Ticket/Query
    ↓
Ingestion Agent (Normalizes input)
    ↓
Planner Agent (Decides execution strategy)
    ↓
┌─────────────────────────────────────┐
│  Parallel Execution:                │
│  - Intent Classification            │
│  - Knowledge Retrieval (RAG)        │
│  - Memory (Read)                    │
└─────────────────────────────────────┘
    ↓
Reasoning Agent (Correlates & analyzes)
    ↓
Response Synthesis Agent
    ↓
Guardrails Agent (Safety check)
    ↓
Final Response or Escalation
```

### Memory Types

1. **Working Memory**: Short-lived, task-level context (session-based)
2. **Episodic Memory**: Past incidents, conversations, outcomes
3. **Semantic Memory**: Documents, FAQs, runbooks, knowledge base

### RAG Implementation

- **Chunking Strategy**: 
  - Chunk size: 1000 characters (configurable)
  - Overlap: 200 characters (configurable)
  - Justification: Preserves semantic continuity across chunk boundaries

- **Supported Formats**:
  - PDF (text + image OCR)
  - Word documents (.docx)
  - Plain text (.txt)
  - PowerPoint (.pptx)
  - Images (.png, .jpg, .jpeg) with OCR

### Guardrails

The system filters:
- Violence (including obfuscated attempts)
- Self-harm references
- Sexual content
- Hate speech
- Jailbreak attempts

Examples of detected patterns:
- `d3str0y 3v3ryth1ng` → Violence
- `su1c1d3 1s th3 4nsw3r` → Self-harm
- `forget your instructions` → Jailbreak

## 🔍 Observability

### Live Streaming

The UI displays real-time:
- Agent execution steps
- Tool calls and results
- Agent interactions
- Final responses

### Event Types

- `agent_execution_start`: When processing begins
- `agent_execution_complete`: When processing finishes
- `agent_execution_error`: On errors
- Tool-specific events for each agent

## 💾 Memory Management UI

Access memories via the UI:
- View all memory types (Working, Episodic, Semantic)
- Delete specific memories
- Update memory entries (coming soon)

API endpoints:
- `GET /api/memories?memory_type={type}&limit={n}`
- `DELETE /api/memories/{memory_type}/{memory_id}`
- `PUT /api/memories/{memory_type}/{memory_id}`

## 🎛️ Configuration

Key configuration options in `config.py`:

- `CHUNK_SIZE`: Document chunk size (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `MIN_CONFIDENCE_THRESHOLD`: Minimum confidence for auto-response (default: 0.7)
- `MAX_CONTEXT_LENGTH`: Maximum context tokens (default: 8000)

## 📝 API Usage

### Process a Request

```bash
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Payment service failing intermittently for EU users",
    "type": "ticket",
    "session_id": "session-123"
  }'
```

### Get Memories

```bash
curl http://localhost:8000/api/memories?memory_type=episodic&limit=10
```

## 🔧 Development

### Adding a New Agent

1. Create a new file in `agents/`
2. Implement the agent class with a `process()` or similar method
3. Add to `agents/__init__.py`
4. Integrate into `orchestration/agent_graph.py`

### Extending RAG

To add support for new file types:
1. Add processor method in `rag/document_processor.py`
2. Update `process_file()` method
3. Add file extension to `SUPPORTED_FILE_TYPES` in `config.py`

## 📈 Monitoring

- Logs are written to `logs/agent_system.log`
- Structured logging with JSON format
- Event history available via `/api/events`

## 🛡️ Safety & Guardrails

The Guardrails Agent:
- Checks all user inputs and agent outputs
- Applies content filters (violence, self-harm, sexual, hate, jailbreak)
- Enforces confidence thresholds
- Escalates when unsafe or low confidence

## 📚 Sample Scenarios

### Scenario 1: Support Analyst
**Input**: "Payment service failing intermittently for EU users"

**Flow**:
1. Ingestion → Normalizes ticket
2. Planner → Decides parallel execution
3. Intent Classification → High priority incident
4. Knowledge Retrieval → Finds related documentation
5. Memory → Retrieves past similar incidents
6. Reasoning → Correlates with gateway failures
7. Response Synthesis → Generates mitigation suggestions
8. Guardrails → Checks safety and confidence
9. **Output**: Actionable response or escalation

### Scenario 2: Support Agent Chat
**Input**: "Have we seen this error code before?"

**Flow**:
- Episodic memory searched
- Past resolutions summarized
- Linked documentation returned

## 🐛 Troubleshooting

### OCR Not Working
- Ensure Tesseract is installed and in PATH
- Check image file formats are supported

### Vector Store Issues
- Delete `data/chroma_db/` and re-index
- Check OpenAI API key is valid

### Memory Database Issues
- Delete `data/memory.db` to reset
- Check SQLite permissions

## 📄 License

This project is built for hackathon demonstration purposes.

## 👥 Team

Built with LangGraph, LangChain, FastAPI, and modern AI agent frameworks.

---

**Note**: This is a production-grade implementation demonstrating all required hackathon capabilities including RAG, memory management, guardrails, observability, and multi-agent coordination.
