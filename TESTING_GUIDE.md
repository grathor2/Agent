# Phased Testing Guide

## Overview

This guide walks you through testing the Collaborative Agent System in 8 phases, from basic environment checks to full end-to-end testing.

## Prerequisites

Before starting, ensure you have:

1. ✅ Python 3.9+ installed
2. ✅ OpenAI API key (already configured)
3. ✅ All dependencies installed

## Setup Steps

### 1. Create Environment File

The `.env` file has been created with your API key. If needed, you can recreate it:

```bash
./setup_env.sh
```

Or manually create `.env` with:
```
# (API key removed for public repo)
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Phased Testing

```bash
python phased_testing.py
```

## Testing Phases

### Phase 1: Environment & Dependencies ✅
- Checks Python version
- Verifies .env file exists
- Validates API key
- Checks required packages are installed

**Expected**: All checks pass

### Phase 2: Core Components ✅
- Imports all 8 agents
- Imports RAG components
- Imports Memory components
- Imports Orchestration components
- Imports Observability components

**Expected**: All imports successful

### Phase 3: Component Initialization ✅
- Initializes Memory Store
- Initializes Document Processor
- Initializes Vector Store
- Initializes Agents

**Expected**: All components initialize without errors

### Phase 4: Individual Agent Testing ✅
- Tests Ingestion Agent
- Tests Guardrails Agent (normal case)
- Tests Guardrails Agent (violation detection)

**Expected**: All agent tests pass

### Phase 5: Memory System Testing ✅
- Tests Working Memory (write/read)
- Tests Episodic Memory (write)
- Tests Semantic Memory (write/read)

**Expected**: All memory operations successful

### Phase 6: RAG System Testing ✅
- Tests Document Processor initialization
- Tests Vector Store initialization
- Notes that full RAG requires indexed documents

**Expected**: RAG components initialize successfully

### Phase 7: Orchestration Testing ✅
- Initializes Orchestrator
- Tests with simple query
- Verifies end-to-end agent flow

**Expected**: Orchestrator processes request successfully

### Phase 8: Full System End-to-End ✅
- Tests Scenario 1: Support Ticket
- Tests Scenario 2: Support Query
- Verifies complete agent pipeline

**Expected**: Both scenarios process successfully

## What Each Phase Tests

### Phase 1-3: Foundation
These phases ensure the basic infrastructure is working:
- Environment setup
- Package installation
- Component imports
- Initialization

### Phase 4-6: Individual Components
These phases test each component in isolation:
- Agent functionality
- Memory operations
- RAG capabilities

### Phase 7-8: Integration
These phases test the complete system:
- Agent orchestration
- End-to-end workflows
- Real-world scenarios

## Expected Output

```
======================================================================
COLLABORATIVE AGENT SYSTEM - PHASED TESTING
======================================================================

======================================================================
PHASE 1: Environment & Dependencies Check
======================================================================
✅ Python version: 3.14.2
✅ .env file exists
✅ OpenAI API key found
✅ Package installed: langgraph
...

======================================================================
TESTING SUMMARY
======================================================================
✅ PASSED: Environment Check
✅ PASSED: Component Import
✅ PASSED: Component Initialization
✅ PASSED: Individual Agents
✅ PASSED: Memory System
✅ PASSED: RAG System
✅ PASSED: Orchestration
✅ PASSED: Full System

Total: 8/8 phases passed

🎉 All phases passed! System is ready.
```

## Troubleshooting

### Phase 1 Fails
- **Issue**: Missing packages
- **Solution**: Run `pip install -r requirements.txt`

### Phase 2 Fails
- **Issue**: Import errors
- **Solution**: Check Python path, ensure all files are present

### Phase 3 Fails
- **Issue**: Initialization errors
- **Solution**: Check API key, database permissions

### Phase 4-6 Fail
- **Issue**: Component-specific errors
- **Solution**: Check logs, verify component configuration

### Phase 7-8 Fail
- **Issue**: Orchestration or API errors
- **Solution**: Check API key validity, network connection, OpenAI API status

## Next Steps After Testing

Once all phases pass:

1. **Generate Test Data**:
   ```bash
   python tests/generate_test_data.py
   ```

2. **Index Knowledge Base**:
   ```bash
   python setup_knowledge_base.py
   ```

3. **Start the Server**:
   ```bash
   python run.py
   ```

4. **Access UI**: http://localhost:8000

## Notes

- Phase 7-8 make actual API calls to OpenAI (costs apply)
- Some phases may take time (especially orchestration)
- All tests are designed to be non-destructive
- Test data is created in isolated test sessions
