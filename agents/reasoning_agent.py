"""Reasoning/Correlation Agent - Connects issues with history."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    from langchain.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

class ReasoningAgent:
    """Correlates current issues with history and identifies patterns."""
    
    def __init__(self):
        self.name = "reasoning_agent"
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.4,
            openai_api_key=OPENAI_API_KEY
        )
        logger.info("ReasoningAgent initialized")
    
    def reason(
        self,
        normalized_input: Dict[str, Any],
        intent_classification: Dict[str, Any],
        knowledge_retrieval: Dict[str, Any],
        memory_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform reasoning and correlation."""
        logger.info("Reasoning started", input_id=normalized_input.get("id"))
        
        # Prepare context
        context_parts = []
        
        # Add intent classification
        if intent_classification.get("status") == "success":
            context_parts.append(f"Intent: {intent_classification['output'].get('intent')}")
            context_parts.append(f"Urgency: {intent_classification['output'].get('urgency')}")
        
        # Add retrieved knowledge
        if knowledge_retrieval.get("status") == "success":
            docs = knowledge_retrieval['output'].get('retrieved_documents', [])
            context_parts.append(f"Retrieved Knowledge ({len(docs)} documents):")
            for doc in docs[:3]:  # Limit context
                context_parts.append(f"- {doc.get('content', '')[:200]}")
        
        # Add memory context
        if memory_data.get("status") == "success":
            episodic = memory_data['output'].get('episodic', [])
            if episodic:
                context_parts.append(f"Past Incidents ({len(episodic)} found):")
                for incident in episodic[:2]:
                    context_parts.append(f"- {incident.get('content', '')[:200]}")
        
        context = "\n".join(context_parts)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a reasoning agent that correlates current issues with historical data.
            Analyze the provided context and:
            1. Identify patterns and root causes
            2. Correlate with past incidents
            3. Suggest mitigation strategies
            4. Assess confidence in your analysis
            
            Return JSON:
            {{
                "patterns": ["pattern1", "pattern2"],
                "root_causes": ["cause1", "cause2"],
                "correlations": [{{"past_incident": "description", "similarity": float}}],
                "mitigation_suggestions": ["suggestion1", "suggestion2"],
                "confidence": float,
                "reasoning": "detailed explanation"
            }}"""),
            ("human", """Current Issue: {current_issue}
            
Context:
{context}

Analyze and provide reasoning.""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "current_issue": normalized_input.get("content", ""),
                "context": context
            })
            
            import json
            content = response.content
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            
            reasoning_result = json.loads(content)
            
            logger.info("Reasoning completed", 
                       confidence=reasoning_result.get("confidence"))
            
            return {
                "agent": self.name,
                "status": "success",
                "output": reasoning_result,
                "tool_calls": [{
                    "tool": "llm",
                    "input": {"current_issue": normalized_input.get("content")},
                    "output": reasoning_result
                }],
                "execution_time": 1.2
            }
        except Exception as e:
            logger.error("Reasoning failed", error=str(e))
            return {
                "agent": self.name,
                "status": "error",
                "output": {"error": str(e)},
                "tool_calls": [],
                "execution_time": 0.1
            }
