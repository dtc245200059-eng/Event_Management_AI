"""
Requirement Analysis Agent (Analyst Agent) for Event Management AI.
Analyzes natural language user inquiries and extracts structured criteria for event discovery.
"""
import time
import re
from pathlib import Path
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.models.agent_message import AgentMessage
from app.services.multi_agent.agent_llm import call_agent_llm_json

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "multi_agent" / "requirement_prompt.txt"

class RequirementAgent(BaseAgent):
    """
    Analyst Agent: Translates free-form user event queries into structured requirement JSON.
    """
    def __init__(self):
        super().__init__("requirement_agent")

    def _fallback_parse(self, text: str) -> Dict[str, Any]:
        """Heuristic rule-based fallback extractor for offline/deterministic scenarios."""
        t_low = text.lower()
        
        # Category detection
        category = None
        if any(w in t_low for w in ["công nghệ", "tech", "ai", "lập trình", "software", "hackathon"]):
            category = "Công nghệ"
        elif any(w in t_low for w in ["kinh doanh", "business", "start-up", "khởi nghiệp", "marketing"]):
            category = "Kinh doanh"
        elif any(w in t_low for w in ["giáo dục", "tốt nghiệp", "hội thảo khoa học", "học thuật"]):
            category = "Giáo dục"

        # Format detection
        fmt = None
        if any(w in t_low for w in ["online", "trực tuyến", "zoom", "livestream"]):
            fmt = "online"
        elif any(w in t_low for w in ["trực tiếp", "offline", "in_person", "tại chỗ"]):
            fmt = "in_person"
        elif "hybrid" in t_low or "kết hợp" in t_low:
            fmt = "hybrid"

        # City detection
        city = None
        if any(w in t_low for w in ["hồ chí minh", "tp.hcm", "tphcm", "sài gòn", "quận 1", "quận 7"]):
            city = "TP. Hồ Chí Minh"
        elif any(w in t_low for w in ["hà nội", "hn", "cầu giấy"]):
            city = "Hà Nội"
        elif any(w in t_low for w in ["đà nẵng", "dn"]):
            city = "Đà Nẵng"
        elif any(w in t_low for w in ["thái nguyên", "ictu"]):
            city = "Thái Nguyên"

        # Max Price extraction
        max_price = None
        if any(w in t_low for w in ["miễn phí", "free", "0 đồng", "0d", "0đ"]):
            max_price = 0
        else:
            price_match = re.search(r'(?:dưới|tối đa|budget|ngân sách|khoảng)?\s*(\d+(?:[.,]\d+)?)\s*(triệu|tr|nghìn|k|vnđ|vnd|đ)', t_low)
            if price_match:
                val = float(price_match.group(1).replace(',', '.'))
                unit = price_match.group(2)
                if unit in ('triệu', 'tr'):
                    max_price = int(val * 1_000_000)
                elif unit in ('nghìn', 'k'):
                    max_price = int(val * 1_000)
                else:
                    max_price = int(val)

        # Topics
        topics = []
        for kw in ["ai", "genai", "machine learning", "cloud", "security", "startup", "blockchain", "data"]:
            if kw in t_low:
                topics.append(kw.upper())

        # Speaker detection
        speaker = None
        spk_match = re.search(r'(?:diễn giả|speaker|thầy|cô|tiến sĩ|ts|pgs)\s+([A-ZÀ-Ỹ][a-zà-ỹ]+(?:\s+[A-ZÀ-Ỹ][a-zà-ỹ]+){1,3})', text)
        if spk_match:
            speaker = spk_match.group(1)

        return {
            "intent": "event_search",
            "category": category,
            "format": fmt,
            "city": city,
            "max_price": max_price,
            "min_capacity": None,
            "topics": topics,
            "speaker": speaker,
            "target_audience": "sinh viên" if "sinh viên" in t_low else None
        }

    def process(self, message: AgentMessage) -> AgentMessage:
        start_time = time.time()
        question = ""
        if isinstance(message.payload, dict):
            question = message.payload.get("question", "")
        elif isinstance(message.payload, str):
            question = message.payload

        if not question:
            question = str(message.payload)

        # Load prompt template
        template = ""
        if PROMPT_PATH.exists():
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                template = f.read()

        prompt = template.replace("{{user_question}}", question) if template else f"Phân tích câu hỏi: {question}"

        default_result = self._fallback_parse(question)
        extracted, mode = call_agent_llm_json(prompt, default_dict=default_result)

        # Merge extracted with fallback to guarantee structure completeness
        final_criteria = dict(default_result)
        for k, v in extracted.items():
            if v is not None and v != "":
                final_criteria[k] = v

        final_criteria["original_question"] = question
        latency = (time.time() - start_time) * 1000

        return self.create_response(
            request_message=message,
            to_agent="orchestrator_agent",
            message_type="event_requirements",
            payload=final_criteria,
            latency_ms=latency
        )
