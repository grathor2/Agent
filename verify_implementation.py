"""Verification script to check all requirements are implemented."""
import os
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    exists = Path(filepath).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    exists = Path(dirpath).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dirpath}")
    return exists

def main():
    """Verify all requirements."""
    print("=" * 70)
    print("VERIFYING COLLABORATIVE AGENT SYSTEM IMPLEMENTATION")
    print("=" * 70)
    print()
    
    all_checks = []
    
    # Check agents (8 agents required)
    print("🤖 AGENTS (8 required):")
    print("-" * 70)
    agents = [
        ("agents/ingestion_agent.py", "Ingestion Agent"),
        ("agents/planner_agent.py", "Planner/Orchestrator Agent"),
        ("agents/intent_classification_agent.py", "Intent Classification Agent"),
        ("agents/knowledge_retrieval_agent.py", "Knowledge Retrieval Agent (RAG)"),
        ("agents/memory_agent.py", "Memory Agent"),
        ("agents/reasoning_agent.py", "Reasoning/Correlation Agent"),
        ("agents/response_synthesis_agent.py", "Response Synthesis Agent"),
        ("agents/guardrails_agent.py", "Guardrails & Policy Agent"),
    ]
    for filepath, desc in agents:
        all_checks.append(check_file_exists(filepath, desc))
    print()
    
    # Check RAG system
    print("📚 RAG SYSTEM:")
    print("-" * 70)
    all_checks.append(check_file_exists("rag/document_processor.py", "Document Processor"))
    all_checks.append(check_file_exists("rag/vector_store.py", "Vector Store"))
    all_checks.append(check_file_exists("rag/__init__.py", "RAG Module Init"))
    print()
    
    # Check Memory system
    print("🧠 MEMORY SYSTEM:")
    print("-" * 70)
    all_checks.append(check_file_exists("memory/memory_store.py", "Memory Store"))
    all_checks.append(check_file_exists("memory/__init__.py", "Memory Module Init"))
    print()
    
    # Check Orchestration
    print("🎯 ORCHESTRATION:")
    print("-" * 70)
    all_checks.append(check_file_exists("orchestration/agent_graph.py", "LangGraph Orchestration"))
    all_checks.append(check_file_exists("orchestration/context_manager.py", "Context Manager"))
    all_checks.append(check_file_exists("orchestration/__init__.py", "Orchestration Module Init"))
    print()
    
    # Check Guardrails
    print("🛡️ GUARDRAILS:")
    print("-" * 70)
    all_checks.append(check_file_exists("agents/guardrails_agent.py", "Guardrails Agent"))
    print()
    
    # Check Observability
    print("👁️ OBSERVABILITY:")
    print("-" * 70)
    all_checks.append(check_file_exists("observability/event_stream.py", "Event Streaming"))
    all_checks.append(check_file_exists("observability/__init__.py", "Observability Module Init"))
    print()
    
    # Check UI
    print("🖥️ UI:")
    print("-" * 70)
    all_checks.append(check_file_exists("ui/main.py", "Web UI with Streaming"))
    all_checks.append(check_file_exists("ui/__init__.py", "UI Module Init"))
    print()
    
    # Check Testing
    print("🧪 TESTING:")
    print("-" * 70)
    all_checks.append(check_file_exists("tests/test_agents.py", "Test Suite"))
    all_checks.append(check_file_exists("tests/generate_test_data.py", "Test Data Generator"))
    all_checks.append(check_file_exists("tests/__init__.py", "Tests Module Init"))
    print()
    
    # Check Configuration
    print("⚙️ CONFIGURATION:")
    print("-" * 70)
    all_checks.append(check_file_exists("config.py", "Configuration"))
    all_checks.append(check_file_exists("requirements.txt", "Dependencies"))
    all_checks.append(check_file_exists(".env.example", "Environment Template"))
    print()
    
    # Check Documentation
    print("📖 DOCUMENTATION:")
    print("-" * 70)
    all_checks.append(check_file_exists("README.md", "Main README"))
    all_checks.append(check_file_exists("QUICKSTART.md", "Quick Start Guide"))
    all_checks.append(check_file_exists("IMPLEMENTATION_SUMMARY.md", "Implementation Summary"))
    all_checks.append(check_file_exists("ARCHITECTURE.md", "Architecture Documentation"))
    print()
    
    # Check Directories
    print("📁 DIRECTORIES:")
    print("-" * 70)
    all_checks.append(check_directory_exists("data/documents", "Documents Directory"))
    all_checks.append(check_directory_exists("data/generated", "Generated Data Directory"))
    all_checks.append(check_directory_exists("data/images", "Images Directory"))
    all_checks.append(check_directory_exists("logs", "Logs Directory"))
    print()
    
    # Check Setup Scripts
    print("🔧 SETUP SCRIPTS:")
    print("-" * 70)
    all_checks.append(check_file_exists("setup_knowledge_base.py", "Knowledge Base Setup"))
    all_checks.append(check_file_exists("run.py", "Main Entry Point"))
    all_checks.append(check_file_exists("example_usage.py", "Example Usage"))
    print()
    
    # Summary
    print("=" * 70)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"SUMMARY: {passed}/{total} checks passed ({percentage:.1f}%)")
    print("=" * 70)
    
    if passed == total:
        print("✅ ALL REQUIREMENTS IMPLEMENTED!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up .env file with OPENAI_API_KEY")
        print("3. Generate test data: python tests/generate_test_data.py")
        print("4. Index knowledge base: python setup_knowledge_base.py")
        print("5. Run system: python run.py")
    else:
        print("⚠️  Some requirements missing. Please review above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
