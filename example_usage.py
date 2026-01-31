"""Example usage of the collaborative agent system."""
import asyncio
from orchestration import AgentOrchestrator

async def main():
    """Example usage."""
    orchestrator = AgentOrchestrator()
    
    # Example 1: Support Ticket
    print("=" * 60)
    print("Example 1: Support Ticket")
    print("=" * 60)
    
    ticket = {
        "content": "Payment service failing intermittently for EU users",
        "type": "ticket",
        "priority": "high",
        "session_id": "session-001"
    }
    
    result = await orchestrator.process_async(ticket)
    print(f"\nFinal Response: {result.get('final_response', {})}")
    print(f"Action: {result.get('final_response', {}).get('action', 'unknown')}")
    
    # Example 2: Support Query
    print("\n" + "=" * 60)
    print("Example 2: Support Query")
    print("=" * 60)
    
    query = {
        "content": "Have we seen this error code before?",
        "type": "query",
        "session_id": "session-002"
    }
    
    result = await orchestrator.process_async(query)
    print(f"\nFinal Response: {result.get('final_response', {})}")
    
    # Example 3: Customer Self-Service
    print("\n" + "=" * 60)
    print("Example 3: Customer Self-Service")
    print("=" * 60)
    
    customer_query = {
        "content": "Why is my dashboard not loading?",
        "type": "query",
        "session_id": "session-003"
    }
    
    result = await orchestrator.process_async(customer_query)
    print(f"\nFinal Response: {result.get('final_response', {})}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
