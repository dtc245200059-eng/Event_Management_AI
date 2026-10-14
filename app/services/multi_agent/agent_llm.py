"""
Agent LLM Invocation Helper.
Provides text generation and robust JSON extraction with multi-model fallback.
"""
import os
import json
import re
from typing import Dict, Any, Optional, Tuple
from app.services.gemini_service import call_gemini

def clean_json_text(raw_text: str) -> str:
    """Extracts JSON string from markdown code fences or surrounding text."""
    text = raw_text.strip()
    # Match markdown code block ```json ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    
    # Try finding first { and last }
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        return text[first_brace:last_brace+1].strip()
        
    return text

def call_agent_llm(prompt: str, system_instruction: Optional[str] = None) -> Tuple[str, str]:
    """Invokes LLM and returns (response_text, mode)."""
    return call_gemini(prompt, system_instruction=system_instruction)

def call_agent_llm_json(prompt: str, system_instruction: Optional[str] = None, default_dict: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], str]:
    """Invokes LLM and safely parses JSON response."""
    text, mode = call_gemini(prompt, system_instruction=system_instruction)
    cleaned = clean_json_text(text)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data, mode
    except Exception:
        pass
    
    return default_dict or {}, mode
