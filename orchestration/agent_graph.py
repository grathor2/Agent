"""LangGraph orchestration for multi-agent system."""
from typing import Dict, Any, List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from operator import add
import asyncio
from agents import (
    IngestionAgent, PlannerAgent, IntentClassificationAgent,
    KnowledgeRetrievalAgent, MemoryAgent, ReasoningAgent,
    ResponseSynthesisAgent, GuardrailsAgent
)
from observability import event_stream
from utils.logger import get_logger

logger = get_logger(__name__)

class AgentState(TypedDict):
    """State for agent graph."""
    input: Dict[str, Any]
    normalized_input: Dict[str, Any]
    plan: Dict[str, Any]
    intent_classification: Dict[str, Any]
    knowledge_retrieval: Dict[str, Any]
    memory_data: Dict[str, Any]
    reasoning: Dict[str, Any]
    response_synthesis: Dict[str, Any]
    guardrails: Dict[str, Any]
    final_response: Dict[str, Any]
    execution_log: Annotated[List[Dict[str, Any]], add]
    errors: Annotated[List[str], add]

class AgentOrchestrator:
    """Orchestrates agent execution using LangGraph."""
    
    def __init__(self):
        self.ingestion_agent = IngestionAgent()
        self.planner_agent = PlannerAgent()
        self.intent_agent = IntentClassificationAgent()
        self.knowledge_agent = KnowledgeRetrievalAgent()
        self.memory_agent = MemoryAgent()
        self.reasoning_agent = ReasoningAgent()
        self.synthesis_agent = ResponseSynthesisAgent()
        self.guardrails_agent = GuardrailsAgent()
        
        self.graph = self._build_graph()
        logger.info("AgentOrchestrator initialized")
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph state graph."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("ingestion", self._ingestion_node)
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("intent_classification", self._intent_classification_node)
        workflow.add_node("knowledge_retrieval", self._knowledge_retrieval_node)
        workflow.add_node("memory", self._memory_node)
        workflow.add_node("reasoning", self._reasoning_node)
        workflow.add_node("response_synthesis", self._response_synthesis_node)
        workflow.add_node("guardrails", self._guardrails_node)
        
        # Define edges
        workflow.set_entry_point("ingestion")
        workflow.add_edge("ingestion", "planner")
        
        # After planner, run three agents in parallel
        workflow.add_edge("planner", "intent_classification")
        workflow.add_edge("planner", "knowledge_retrieval")
        workflow.add_edge("planner", "memory")
        
        # All three parallel agents feed into reasoning
        workflow.add_edge("intent_classification", "reasoning")
        workflow.add_edge("knowledge_retrieval", "reasoning")
        workflow.add_edge("memory", "reasoning")
        
        # Reasoning to synthesis
        workflow.add_edge("reasoning", "response_synthesis")
        
        # Synthesis to guardrails
        workflow.add_edge("response_synthesis", "guardrails")
        
        # Guardrails decides final action
        workflow.add_conditional_edges(
            "guardrails",
            self._route_after_guardrails,
            {
                "auto": END,
                "escalate": END
            }
        )
        
        return workflow.compile()
    
    async def _ingestion_node(self, state: AgentState) -> AgentState:
        """Ingestion agent node."""
        logger.info("Executing ingestion node")
        await event_stream.emit("agent_start", {"agent": "ingestion", "input": state["input"]})
        result = self.ingestion_agent.process(state["input"])
        state["normalized_input"] = result["output"]
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "ingestion", "result": result})
        return state
    
    async def _planner_node(self, state: AgentState) -> AgentState:
        """Planner agent node."""
        logger.info("Executing planner node")
        await event_stream.emit("agent_start", {"agent": "planner", "input": state["normalized_input"]})
        result = self.planner_agent.plan(state["normalized_input"])
        state["plan"] = result["output"]
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "planner", "result": result})
        return state
    
    async def _intent_classification_node(self, state: AgentState) -> AgentState:
        """Intent classification node."""
        logger.info("Executing intent classification node")
        await event_stream.emit("agent_start", {"agent": "intent_classification", "input": state["normalized_input"]})
        result = self.intent_agent.classify(state["normalized_input"])
        state["intent_classification"] = result
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "intent_classification", "result": result})
        return state
    
    async def _knowledge_retrieval_node(self, state: AgentState) -> AgentState:
        """Knowledge retrieval node."""
        logger.info("Executing knowledge retrieval node")
        await event_stream.emit("agent_start", {"agent": "knowledge_retrieval", "input": state["normalized_input"]})
        result = self.knowledge_agent.retrieve(state["normalized_input"])
        state["knowledge_retrieval"] = result
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "knowledge_retrieval", "result": result})
        return state
    
    async def _memory_node(self, state: AgentState) -> AgentState:
        """Memory agent node."""
        logger.info("Executing memory node")
        await event_stream.emit("agent_start", {"agent": "memory", "input": state["normalized_input"]})
        result = self.memory_agent.read_memory(state["normalized_input"])
        state["memory_data"] = result
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "memory", "result": result})
        return state
    
    async def _reasoning_node(self, state: AgentState) -> AgentState:
        """Reasoning node."""
        logger.info("Executing reasoning node")
        await event_stream.emit("agent_start", {"agent": "reasoning", "input": state["normalized_input"]})
        result = self.reasoning_agent.reason(
            state["normalized_input"],
            state.get("intent_classification", {}),
            state.get("knowledge_retrieval", {}),
            state.get("memory_data", {})
        )
        state["reasoning"] = result
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "reasoning", "result": result})
        return state
    
    async def _response_synthesis_node(self, state: AgentState) -> AgentState:
        """Response synthesis node."""
        logger.info("Executing response synthesis node")
        await event_stream.emit("agent_start", {"agent": "response_synthesis", "input": state["normalized_input"]})
        result = self.synthesis_agent.synthesize(
            state["normalized_input"],
            state.get("intent_classification", {}),
            state.get("knowledge_retrieval", {}),
            state.get("reasoning", {})
        )
        state["response_synthesis"] = result
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "response_synthesis", "result": result})
        return state
    
    async def _guardrails_node(self, state: AgentState) -> AgentState:
        """Guardrails node."""
        logger.info("Executing guardrails node")
        await event_stream.emit("agent_start", {"agent": "guardrails", "input": state["response_synthesis"]})
        user_input = state["normalized_input"].get("content", "")
        result = self.guardrails_agent.check(state["response_synthesis"], user_input)
        state["guardrails"] = result
        
        # Set final response
        if result["output"]["action"] == "auto":
            state["final_response"] = {
                "response": result["output"]["safe_response"],
                "action": "auto",
                "confidence": result["output"]["confidence"]
            }
        else:
            state["final_response"] = {
                "response": "This request requires human review. It has been escalated.",
                "action": "escalate",
                "escalation_reason": result["output"]["escalation_reason"],
                "violations": result["output"]["violations"]
            }
        
        state["execution_log"].append(result)
        await event_stream.emit("agent_complete", {"agent": "guardrails", "result": result})
        await event_stream.emit("final_response", {"response": state["final_response"]})
        return state
    
    def _route_after_guardrails(self, state: AgentState) -> str:
        """Route after guardrails based on action."""
        guardrails = state.get("guardrails", {})
        action = guardrails.get("output", {}).get("action", "escalate")
        return action
    
    async def process_async(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input asynchronously."""
        # Create a copy to avoid state mutation issues
        input_copy = dict(input_data) if isinstance(input_data, dict) else {"content": str(input_data)}
        
        initial_state: AgentState = {
            "input": input_copy,
            "normalized_input": {},
            "plan": {},
            "intent_classification": {},
            "knowledge_retrieval": {},
            "memory_data": {},
            "reasoning": {},
            "response_synthesis": {},
            "guardrails": {},
            "final_response": {},
            "execution_log": [],
            "errors": []
        }
        
        try:
            final_state = await self.graph.ainvoke(initial_state)
            return final_state
        except Exception as e:
            logger.error("Orchestration failed", error=str(e))
            if "errors" not in initial_state:
                initial_state["errors"] = []
            initial_state["errors"].append(str(e))
            return initial_state
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input synchronously."""
        return asyncio.run(self.process_async(input_data))
