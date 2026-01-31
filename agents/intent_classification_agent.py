"""Intent & Classification Agent - Detects intent, urgency, SLA risk."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    from langchain.prompts import ChatPromptTemplate
from config import MODEL_NAME, OPENAI_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

class IntentClassificationAgent:
    """Classifies intent, urgency, and risk."""
    
    def __init__(self):
        self.name = "intent_classification_agent"
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.2,
            openai_api_key=OPENAI_API_KEY
        )
        logger.info("IntentClassificationAgent initialized")
    
    def classify(self, normalized_input: Dict[str, Any]) -> Dict[str, Any]:
        """Classify intent, urgency, and risk."""
        logger.info("Classification started", input_id=normalized_input.get("id"))
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intent classification agent for support tickets.
            Analyze the input and classify:
            1. Intent: What is the user trying to achieve? (e.g., "incident_report", "question", "request", "complaint")
            2. Urgency: Low, Medium, High, Critical
            3. SLA Risk: Will this breach SLA? (yes/no with confidence)
            4. Category: Technical, Billing, Account, General
            5. Confidence: 0.0 to 1.0
            
            Return JSON:
            {{
                "intent": "string",
                "urgency": "low|medium|high|critical",
                "sla_risk": {{"breach_likely": bool, "confidence": float, "reason": "string"}},
                "category": "string",
                "confidence": float,
                "keywords": ["keyword1", "keyword2"]
            }}"""),
            ("human", "Input: {content}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "content": normalized_input.get("content", "")
            })
            
            import json
            content = response.content
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            
            classification = json.loads(content)
            
            logger.info("Classification completed", 
                       intent=classification.get("intent"),
                       urgency=classification.get("urgency"))
            
            return {
                "agent": self.name,
                "status": "success",
                "output": classification,
                "tool_calls": [{"tool": "llm", "input": normalized_input, "output": classification}],
                "execution_time": 0.8
            }
        except Exception as e:
            logger.error("Classification failed", error=str(e))
            return {
                "agent": self.name,
                "status": "error",
                "output": {"error": str(e)},
                "tool_calls": [],
                "execution_time": 0.1
            }
