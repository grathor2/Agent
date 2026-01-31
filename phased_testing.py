"""Phased testing script to verify the application step by step."""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_phase_header(phase_num, phase_name):
    """Print phase header."""
    print("\n" + "=" * 70)
    print(f"PHASE {phase_num}: {phase_name}")
    print("=" * 70)

def print_success(message):
    """Print success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print info message."""
    print(f"ℹ️  {message}")

# Phase 1: Environment and Dependencies
def phase1_check_environment():
    """Phase 1: Check environment and dependencies."""
    print_phase_header(1, "Environment & Dependencies Check")
    
    checks = []
    
    # Check Python version
    try:
        import sys
        version = sys.version_info
        if version.major >= 3 and version.minor >= 9:
            print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
            checks.append(True)
        else:
            print_error(f"Python version too old: {version.major}.{version.minor}")
            checks.append(False)
    except Exception as e:
        print_error(f"Could not check Python version: {e}")
        checks.append(False)
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print_success(".env file exists")
        checks.append(True)
    else:
        print_error(".env file not found")
        checks.append(False)
    
    # Check API key
    import os
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and len(api_key) > 20:
        print_success("OpenAI API key found")
        checks.append(True)
    else:
        print_error("OpenAI API key not found or invalid")
        checks.append(False)
    
    # Check required packages
    required_packages = [
        "langgraph", "langchain", "fastapi", "chromadb",
        "pypdf", "python-docx", "pillow", "sqlalchemy"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"Package installed: {package}")
            checks.append(True)
        except ImportError:
            print_error(f"Package missing: {package}")
            checks.append(False)
    
    return all(checks)

# Phase 2: Core Components
def phase2_check_components():
    """Phase 2: Check core components."""
    print_phase_header(2, "Core Components Check")
    
    checks = []
    
    # Check agents
    try:
        from agents import (
            IngestionAgent, PlannerAgent, IntentClassificationAgent,
            KnowledgeRetrievalAgent, MemoryAgent, ReasoningAgent,
            ResponseSynthesisAgent, GuardrailsAgent
        )
        print_success("All 8 agents imported successfully")
        checks.append(True)
    except Exception as e:
        print_error(f"Failed to import agents: {e}")
        checks.append(False)
    
    # Check RAG
    try:
        from rag import DocumentProcessor, VectorStore
        print_success("RAG components imported")
        checks.append(True)
    except Exception as e:
        print_error(f"Failed to import RAG: {e}")
        checks.append(False)
    
    # Check Memory
    try:
        from memory import MemoryStore, MemoryType
        print_success("Memory components imported")
        checks.append(True)
    except Exception as e:
        print_error(f"Failed to import memory: {e}")
        checks.append(False)
    
    # Check Orchestration
    try:
        from orchestration import AgentOrchestrator
        print_success("Orchestration components imported")
        checks.append(True)
    except Exception as e:
        print_error(f"Failed to import orchestration: {e}")
        checks.append(False)
    
    # Check Observability
    try:
        from observability import EventStream, event_stream
        print_success("Observability components imported")
        checks.append(True)
    except Exception as e:
        print_error(f"Failed to import observability: {e}")
        checks.append(False)
    
    return all(checks)

# Phase 3: Initialize Components
def phase3_initialize_components():
    """Phase 3: Initialize components."""
    print_phase_header(3, "Component Initialization")
    
    checks = []
    
    # Initialize Memory Store
    try:
        from memory import MemoryStore
        memory_store = MemoryStore()
        print_success("Memory store initialized")
        checks.append(True)
    except Exception as e:
        print_error(f"Memory store initialization failed: {e}")
        checks.append(False)
    
    # Initialize Document Processor
    try:
        from rag import DocumentProcessor
        processor = DocumentProcessor()
        print_success("Document processor initialized")
        checks.append(True)
    except Exception as e:
        print_error(f"Document processor initialization failed: {e}")
        checks.append(False)
    
    # Initialize Vector Store
    try:
        from rag import VectorStore
        vector_store = VectorStore()
        print_success("Vector store initialized")
        checks.append(True)
    except Exception as e:
        print_error(f"Vector store initialization failed: {e}")
        checks.append(False)
    
    # Initialize Agents
    try:
        from agents import IngestionAgent, GuardrailsAgent
        ingestion = IngestionAgent()
        guardrails = GuardrailsAgent()
        print_success("Agents initialized")
        checks.append(True)
    except Exception as e:
        print_error(f"Agent initialization failed: {e}")
        checks.append(False)
    
    return all(checks)

# Phase 4: Test Individual Agents
def phase4_test_agents():
    """Phase 4: Test individual agents."""
    print_phase_header(4, "Individual Agent Testing")
    
    checks = []
    
    # Test Ingestion Agent
    try:
        from agents import IngestionAgent
        agent = IngestionAgent()
        result = agent.process("Test query for payment service")
        if result["status"] == "success":
            print_success("Ingestion Agent: Processed input successfully")
            checks.append(True)
        else:
            print_error("Ingestion Agent: Failed to process")
            checks.append(False)
    except Exception as e:
        print_error(f"Ingestion Agent test failed: {e}")
        checks.append(False)
    
    # Test Guardrails Agent
    try:
        from agents import GuardrailsAgent
        agent = GuardrailsAgent()
        response_data = {
            "output": {
                "response": "Test response",
                "confidence": 0.8
            }
        }
        result = agent.check(response_data, "normal query")
        if result["status"] == "success":
            print_success("Guardrails Agent: Safety check passed")
            checks.append(True)
        else:
            print_error("Guardrails Agent: Safety check failed")
            checks.append(False)
    except Exception as e:
        print_error(f"Guardrails Agent test failed: {e}")
        checks.append(False)
    
    # Test Guardrails with violation
    try:
        from agents import GuardrailsAgent
        agent = GuardrailsAgent()
        response_data = {
            "output": {
                "response": "Test",
                "confidence": 0.8
            }
        }
        result = agent.check(response_data, "destroy everything")
        violations = result["output"]["violations"]
        if any(v["category"] == "violence" for v in violations):
            print_success("Guardrails Agent: Correctly detected violence")
            checks.append(True)
        else:
            print_error("Guardrails Agent: Failed to detect violation")
            checks.append(False)
    except Exception as e:
        print_error(f"Guardrails violation test failed: {e}")
        checks.append(False)
    
    return all(checks)

# Phase 5: Test Memory System
def phase5_test_memory():
    """Phase 5: Test memory system."""
    print_phase_header(5, "Memory System Testing")
    
    checks = []
    
    try:
        from memory import MemoryStore
        store = MemoryStore()
        
        # Test Working Memory
        store.write_working_memory("test-session", "test_key", {"value": "test_data"})
        result = store.read_working_memory("test-session", "test_key")
        if "test_key" in result and result["test_key"]["value"] == "test_data":
            print_success("Working Memory: Write/Read successful")
            checks.append(True)
        else:
            print_error("Working Memory: Write/Read failed")
            checks.append(False)
        
        # Test Episodic Memory
        memory_id = store.write_episodic_memory(
            event_type="test_incident",
            content="Test incident content",
            conversation_id="test-session"
        )
        if memory_id > 0:
            print_success("Episodic Memory: Write successful")
            checks.append(True)
        else:
            print_error("Episodic Memory: Write failed")
            checks.append(False)
        
        # Test Semantic Memory
        store.write_semantic_memory(
            key="test_knowledge",
            content="Test knowledge content",
            category="test"
        )
        results = store.read_semantic_memory(key="test_knowledge")
        if results and results[0]["key"] == "test_knowledge":
            print_success("Semantic Memory: Write/Read successful")
            checks.append(True)
        else:
            print_error("Semantic Memory: Write/Read failed")
            checks.append(False)
        
    except Exception as e:
        print_error(f"Memory system test failed: {e}")
        checks.append(False)
    
    return all(checks)

# Phase 6: Test RAG System
def phase6_test_rag():
    """Phase 6: Test RAG system."""
    print_phase_header(6, "RAG System Testing")
    
    checks = []
    
    try:
        from rag import DocumentProcessor, VectorStore
        
        # Test Document Processor
        processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
        print_success("Document Processor: Initialized with chunking")
        checks.append(True)
        
        # Test Vector Store
        vector_store = VectorStore()
        print_success("Vector Store: Initialized")
        checks.append(True)
        
        # Note: Full RAG test requires documents to be indexed
        print_info("RAG retrieval test requires indexed documents (run setup_knowledge_base.py)")
        checks.append(True)
        
    except Exception as e:
        print_error(f"RAG system test failed: {e}")
        checks.append(False)
    
    return all(checks)

# Phase 7: Test Orchestration
async def phase7_test_orchestration():
    """Phase 7: Test orchestration."""
    print_phase_header(7, "Orchestration Testing")
    
    checks = []
    
    try:
        from orchestration import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        print_success("Orchestrator: Initialized")
        checks.append(True)
        
        # Test with simple input
        input_data = {
            "content": "Test query for system",
            "type": "query",
            "session_id": "test-session-001"
        }
        
        print_info("Running orchestrator test (this may take a moment)...")
        result = await orchestrator.process_async(input_data)
        
        if "final_response" in result:
            print_success("Orchestrator: Processed request successfully")
            print_info(f"Response action: {result.get('final_response', {}).get('action', 'unknown')}")
            checks.append(True)
        else:
            print_error("Orchestrator: Failed to process request")
            if "errors" in result:
                print_error(f"Errors: {result['errors']}")
            checks.append(False)
        
    except Exception as e:
        print_error(f"Orchestration test failed: {e}")
        import traceback
        traceback.print_exc()
        checks.append(False)
    
    return all(checks)

# Phase 8: Test Full System
async def phase8_test_full_system():
    """Phase 8: Test full system end-to-end."""
    print_phase_header(8, "Full System End-to-End Testing")
    
    checks = []
    
    try:
        from orchestration import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        
        # Test Scenario 1: Support Ticket
        print_info("Testing Scenario 1: Support Ticket")
        ticket = {
            "content": "Payment service failing intermittently for EU users",
            "type": "ticket",
            "priority": "high",
            "session_id": "test-session-001"
        }
        
        result = await orchestrator.process_async(ticket)
        if result.get("final_response"):
            print_success("Scenario 1: Processed successfully")
            print_info(f"  Action: {result['final_response'].get('action')}")
            checks.append(True)
        else:
            print_error("Scenario 1: Failed")
            checks.append(False)
        
        # Test Scenario 2: Query
        print_info("Testing Scenario 2: Support Query")
        query = {
            "content": "Have we seen this error code before?",
            "type": "query",
            "session_id": "test-session-002"
        }
        
        result = await orchestrator.process_async(query)
        if result.get("final_response"):
            print_success("Scenario 2: Processed successfully")
            checks.append(True)
        else:
            print_error("Scenario 2: Failed")
            checks.append(False)
        
    except Exception as e:
        print_error(f"Full system test failed: {e}")
        import traceback
        traceback.print_exc()
        checks.append(False)
    
    return all(checks)

# Main execution
async def main():
    """Run all phases."""
    print("\n" + "=" * 70)
    print("COLLABORATIVE AGENT SYSTEM - PHASED TESTING")
    print("=" * 70)
    
    phases = [
        ("Environment Check", phase1_check_environment, False),
        ("Component Import", phase2_check_components, False),
        ("Component Initialization", phase3_initialize_components, False),
        ("Individual Agents", phase4_test_agents, False),
        ("Memory System", phase5_test_memory, False),
        ("RAG System", phase6_test_rag, False),
        ("Orchestration", phase7_test_orchestration, True),
        ("Full System", phase8_test_full_system, True),
    ]
    
    results = []
    
    for phase_name, phase_func, is_async in phases:
        try:
            if is_async:
                result = await phase_func()
            else:
                result = phase_func()
            results.append((phase_name, result))
            
            if not result:
                print_error(f"\n⚠️  Phase '{phase_name}' had failures. Continuing...")
        except Exception as e:
            print_error(f"\n❌ Phase '{phase_name}' crashed: {e}")
            results.append((phase_name, False))
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 70)
    print("TESTING SUMMARY")
    print("=" * 70)
    
    for phase_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {phase_name}")
    
    total_passed = sum(1 for _, result in results if result)
    total_phases = len(results)
    
    print(f"\nTotal: {total_passed}/{total_phases} phases passed")
    
    if total_passed == total_phases:
        print("\n🎉 All phases passed! System is ready.")
    else:
        print(f"\n⚠️  {total_phases - total_passed} phase(s) had issues. Review above.")
    
    return total_passed == total_phases

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Testing failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
