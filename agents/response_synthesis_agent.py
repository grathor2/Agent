"""Response Synthesis Agent - Generates human-readable outputs."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    from langchain.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

class ResponseSynthesisAgent:
    """Synthesizes final response from all agent outputs."""
    
    def __init__(self):
        self.name = "response_synthesis_agent"
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY
        )
        logger.info("ResponseSynthesisAgent initialized")
    
    def synthesize(
        self,
        normalized_input: Dict[str, Any],
        intent_classification: Dict[str, Any],
        knowledge_retrieval: Dict[str, Any],
        reasoning: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize final response."""
        logger.info("Response synthesis started", 
                   input_id=normalized_input.get("id"))
        
        # Prepare synthesis context
        context_parts = []
        
        if intent_classification.get("status") == "success":
            intent_data = intent_classification['output']
            context_parts.append(f"Intent: {intent_data.get('intent')}, Urgency: {intent_data.get('urgency')}")
        
        if knowledge_retrieval.get("status") == "success":
            docs = knowledge_retrieval['output'].get('retrieved_documents', [])
            context_parts.append(f"Relevant Knowledge: {len(docs)} documents retrieved")
        
        if reasoning.get("status") == "success":
            reasoning_data = reasoning['output']
            context_parts.append(f"Analysis: {reasoning_data.get('reasoning', '')[:500]}")
            if reasoning_data.get('mitigation_suggestions'):
                context_parts.append(f"Suggestions: {', '.join(reasoning_data['mitigation_suggestions'][:3])}")
        
        context = "\n".join(context_parts)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a response synthesis agent for a support system.
            Generate a clear, helpful, and professional response based on the analysis.
            The response should:
            1. Address the user's query directly
            2. Reference relevant knowledge and past incidents when applicable
            3. Provide actionable recommendations
            4. Be concise but comprehensive
            5. Use a professional but friendly tone
            
            Return JSON:
            {{
                "response": "the main response text",
                "recommendations": ["rec1", "rec2"],
                "references": ["ref1", "ref2"],
                "confidence": float
            }}"""),
            ("human", """User Query: {user_query}

Analysis Context:
{context}

Generate a helpful response.""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "user_query": normalized_input.get("content", ""),
                "context": context
            })
            
            import json
            content = response.content
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            
            synthesis_result = json.loads(content)
            
            logger.info("Response synthesis completed", 
                       confidence=synthesis_result.get("confidence"))
            
            return {
                "agent": self.name,
                "status": "success",
                "output": synthesis_result,
                "tool_calls": [{
                    "tool": "llm",
                    "input": {"user_query": normalized_input.get("content")},
                    "output": synthesis_result
                }],
                "execution_time": 1.0
            }
        except Exception as e:
            logger.error("Response synthesis failed", error=str(e))
            return {
                "agent": self.name,
                "status": "error",
                "output": {"error": str(e), "response": "I apologize, but I encountered an error processing your request."},
                "tool_calls": [],
                "execution_time": 0.1
            }
