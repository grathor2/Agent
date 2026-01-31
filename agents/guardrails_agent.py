"""Guardrails & Policy Agent - Applies safety rules and escalation."""
from typing import Dict, Any, List
import re
from config import MIN_CONFIDENCE_THRESHOLD
from utils.logger import get_logger

logger = get_logger(__name__)

class GuardrailsAgent:
    """Applies guardrails and safety policies."""
    
    def __init__(self):
        self.name = "guardrails_agent"
        self.min_confidence = MIN_CONFIDENCE_THRESHOLD
        self._initialize_content_filters()
        logger.info("GuardrailsAgent initialized", 
                   min_confidence=self.min_confidence)
    
    def _initialize_content_filters(self):
        """Initialize content filter patterns."""
        # Violence patterns (with obfuscation detection)
        self.violence_patterns = [
            r'\b(kill|destroy|attack|harm|hurt|violence|assault)\w*\b',
            r'd3str[o0]y|4tt4ck|h3rt|k1ll',
            r'destroy\s+everything|attack\s+now'
        ]
        
        # Self-harm patterns
        self.self_harm_patterns = [
            r'\b(suicide|self.?harm|kill\s+myself|end\s+my\s+life)\w*\b',
            r'su1c1d3|k1ll\s+mys3lf|h3rt\s+mys3lf',
            r'suicide\s+is\s+the\s+answer'
        ]
        
        # Sexual content patterns
        self.sexual_patterns = [
            r'\b(sex|porn|sexual|explicit|nude)\w*\b',
            r's3x|p0rn|s3xu4l',
            r'sex\s+with\s+me|pornographic\s+material'
        ]
        
        # Hate speech patterns
        self.hate_patterns = [
            r'\b(hate|racist|discriminate|immigrant|refugee)\w*\b',
            r'h@t3|r4c1st',
            r'hate\s+immigrants|hate\s+.*group'
        ]
        
        # Jailbreak patterns
        self.jailbreak_patterns = [
            r'forget\s+your\s+instructions?',
            r'ignore\s+previous\s+instructions?',
            r'act\s+as\s+if\s+you\s+are',
            r'pretend\s+to\s+be',
            r'roleplay\s+as',
            r'you\s+are\s+now\s+a'
        ]
    
    def check(self, response_data: Dict[str, Any], user_input: str = "") -> Dict[str, Any]:
        """Check guardrails and apply policies."""
        logger.info("Guardrails check started")
        
        violations = []
        confidence = response_data.get("output", {}).get("confidence", 0.0)
        
        # Check content filters
        content_to_check = user_input.lower() + " " + str(response_data.get("output", {})).lower()
        
        # Violence check
        if self._check_patterns(content_to_check, self.violence_patterns):
            violations.append({
                "category": "violence",
                "severity": "high",
                "message": "Content contains violent language"
            })
        
        # Self-harm check
        if self._check_patterns(content_to_check, self.self_harm_patterns):
            violations.append({
                "category": "self_harm",
                "severity": "critical",
                "message": "Content contains self-harm references"
            })
        
        # Sexual content check
        if self._check_patterns(content_to_check, self.sexual_patterns):
            violations.append({
                "category": "sexual",
                "severity": "high",
                "message": "Content contains sexual references"
            })
        
        # Hate speech check
        if self._check_patterns(content_to_check, self.hate_patterns):
            violations.append({
                "category": "hate",
                "severity": "high",
                "message": "Content contains hate speech"
            })
        
        # Jailbreak check
        if self._check_patterns(content_to_check, self.jailbreak_patterns):
            violations.append({
                "category": "jailbreak",
                "severity": "medium",
                "message": "Potential jailbreak attempt detected"
            })
        
        # Confidence check
        if confidence < self.min_confidence:
            violations.append({
                "category": "low_confidence",
                "severity": "medium",
                "message": f"Confidence {confidence:.2f} below threshold {self.min_confidence}"
            })
        
        # Decision
        should_escalate = len(violations) > 0 or confidence < self.min_confidence
        action = "escalate" if should_escalate else "auto"
        
        if violations:
            logger.warning("Guardrails violations detected", 
                          violations=[v["category"] for v in violations])
        else:
            logger.info("Guardrails check passed", confidence=confidence)
        
        return {
            "agent": self.name,
            "status": "success",
            "output": {
                "action": action,
                "violations": violations,
                "confidence": confidence,
                "escalation_reason": violations[0]["message"] if violations else None,
                "safe_response": response_data.get("output", {}).get("response", "") if not should_escalate else None
            },
            "tool_calls": [{
                "tool": "content_filter",
                "input": {"content_length": len(content_to_check)},
                "output": {"violations_count": len(violations)}
            }],
            "execution_time": 0.1
        }
    
    def _check_patterns(self, text: str, patterns: List[str]) -> bool:
        """Check if text matches any pattern."""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
