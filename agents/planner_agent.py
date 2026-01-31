"""Planner/Orchestrator Agent - Decides execution strategy."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    from langchain.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

class PlannerAgent:
    """Plans execution strategy and delegates tasks."""
    
    def __init__(self):
        self.name = "planner_agent"
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.3,
            openai_api_key=OPENAI_API_KEY
        )
        logger.info("PlannerAgent initialized")
    
    def plan(self, normalized_input: Dict[str, Any]) -> Dict[str, Any]:
        """Create execution plan."""
        logger.info("Planning started", input_id=normalized_input.get("id"))
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a planning agent that decides execution strategy for support tickets.
            Analyze the input and determine:
            1. Which agents need to run (intent_classification, knowledge_retrieval, memory, reasoning)
            2. Execution order (serial, parallel, or async)
            3. Dependencies between agents
            
            Available agents:
            - intent_classification: Detects intent, urgency, SLA risk
            - knowledge_retrieval: Searches knowledge base (RAG)
            - memory: Reads/writes episodic and semantic memory
            - reasoning: Correlates with history and patterns
            
            Return JSON with:
            {{
                "agents_to_run": ["agent1", "agent2"],
                "execution_mode": "serial" | "parallel" | "async",
                "dependencies": {{"agent1": [], "agent2": ["agent1"]}},
                "reasoning": "explanation"
            }}"""),
            ("human", "Input: {input_content}\n\nType: {input_type}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "input_content": normalized_input.get("content", ""),
                "input_type": normalized_input.get("type", "unknown")
            })
            
            import json
            # Parse response (handle both JSON and text)
            content = response.content
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            
            plan = json.loads(content)
            
            logger.info("Planning completed", 
                       agents=plan.get("agents_to_run", []),
                       mode=plan.get("execution_mode"))
            
            return {
                "agent": self.name,
                "status": "success",
                "output": plan,
                "tool_calls": [{"tool": "llm", "input": normalized_input, "output": plan}],
                "execution_time": 0.5
            }
        except Exception as e:
            logger.error("Planning failed", error=str(e))
            # Fallback plan
            default_plan = {
                "agents_to_run": ["intent_classification", "knowledge_retrieval", "memory"],
                "execution_mode": "parallel",
                "dependencies": {},
                "reasoning": "Default parallel execution"
            }
            return {
                "agent": self.name,
                "status": "success",
                "output": default_plan,
                "tool_calls": [],
                "execution_time": 0.1
            }
