# System Architecture

## Overview

The Collaborative Agent System is built using LangGraph for orchestration, with 8 specialized agents working together to process support tickets and queries.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Incoming Request                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Ingestion Agent      │  Normalizes input
            └──────────┬────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Planner Agent        │  Decides execution strategy
            └──────────┬────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Intent     │ │  Knowledge   │ │   Memory     │
│Classification│ │  Retrieval   │ │   Agent      │
│   Agent      │ │   (RAG)      │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────┬────────┴────────┬──────┘
                │                 │
                ▼                 │
       ┌──────────────────────┐   │
       │  Reasoning Agent     │   │  Correlates & analyzes
       └──────────┬───────────┘   │
                  │                │
                  └────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │ Response Synthesis    │  Generates response
            └──────────┬───────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Guardrails Agent     │  Safety check
            └──────────┬───────────┘
                       │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
      ┌─────────┐           ┌──────────────┐
      │   Auto  │           │  Escalate    │
      │ Response│           │  to Human    │
      └─────────┘           └──────────────┘
```

## Component Details

### 1. Ingestion Agent
- **Purpose**: Normalizes incoming tickets/queries
- **Input**: Raw user input (string or dict)
- **Output**: Normalized structure with metadata
- **File**: `agents/ingestion_agent.py`

### 2. Planner Agent
- **Purpose**: Decides execution strategy
- **Capabilities**: 
  - Determines which agents to run
  - Chooses serial/parallel/async execution
  - Identifies dependencies
- **File**: `agents/planner_agent.py`

### 3. Intent Classification Agent
- **Purpose**: Detects intent, urgency, SLA risk
- **Output**: Intent type, urgency level, category, confidence
- **File**: `agents/intent_classification_agent.py`

### 4. Knowledge Retrieval Agent (RAG)
- **Purpose**: Searches knowledge base
- **Technology**: Vector similarity search (ChromaDB)
- **Supports**: PDF, DOCX, TXT, PPTX, Images
- **File**: `agents/knowledge_retrieval_agent.py`

### 5. Memory Agent
- **Purpose**: Manages memory operations
- **Memory Types**:
  - Working: Session-based, short-lived
  - Episodic: Past incidents, conversations
  - Semantic: Knowledge base, FAQs
- **File**: `agents/memory_agent.py`

### 6. Reasoning Agent
- **Purpose**: Correlates current issues with history
- **Capabilities**:
  - Pattern identification
  - Root cause analysis
  - Historical correlation
- **File**: `agents/reasoning_agent.py`

### 7. Response Synthesis Agent
- **Purpose**: Generates human-readable response
- **Input**: All previous agent outputs
- **Output**: Formatted response with recommendations
- **File**: `agents/response_synthesis_agent.py`

### 8. Guardrails Agent
- **Purpose**: Safety and policy enforcement
- **Checks**:
  - Content filtering (violence, self-harm, etc.)
  - Confidence thresholds
  - Escalation policies
- **File**: `agents/guardrails_agent.py`

## Data Flow

### Serial Execution
1. Ingestion → Planner → (Intent/Knowledge/Memory) → Reasoning → Synthesis → Guardrails

### Parallel Execution
After Planner:
- Intent Classification (parallel)
- Knowledge Retrieval (parallel)
- Memory Read (parallel)
- All feed into Reasoning (waits for all)

### Asynchronous Execution
- Memory writes happen asynchronously
- Event streaming for observability
- Logging operations

## Storage

### Vector Store (ChromaDB)
- **Location**: `data/chroma_db/`
- **Purpose**: Document embeddings for RAG
- **Persistence**: Disk-based

### Memory Store (SQLite)
- **Location**: `data/memory.db`
- **Tables**:
  - `working_memory`: Session-based temporary data
  - `episodic_memory`: Past incidents and conversations
  - `semantic_memory`: Knowledge base entries

## Observability

### Event Streaming
- **Technology**: WebSocket
- **Events**: Agent start/complete, tool calls, errors
- **UI**: Real-time display in browser

### Logging
- **Format**: Structured JSON logs
- **Location**: `logs/agent_system.log`
- **Levels**: INFO, WARNING, ERROR, DEBUG

## API Endpoints

- `POST /api/process`: Process a request
- `GET /api/memories`: Get memories
- `DELETE /api/memories/{type}/{id}`: Delete memory
- `PUT /api/memories/{type}/{id}`: Update memory
- `GET /api/events`: Get event history
- `WS /ws`: WebSocket for live streaming

## Configuration

Key settings in `config.py`:
- `CHUNK_SIZE`: 1000 characters
- `CHUNK_OVERLAP`: 200 characters
- `MIN_CONFIDENCE_THRESHOLD`: 0.7
- `MAX_CONTEXT_LENGTH`: 8000 tokens

## Security

- Content filtering for harmful content
- Confidence-based escalation
- Input validation
- Error handling and logging

## Scalability

- Modular agent design
- Stateless agents (except memory)
- Can scale horizontally
- Async operations for performance
