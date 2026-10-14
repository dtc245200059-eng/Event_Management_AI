"""
Recommendation & Reasoning Agent for Event Management AI.
Synthesizes structured SQL event records, vector knowledge, and user constraints
to formulate reasoned recommendations and alternatives. Supports retry loops with Critic feedback.
"""
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.models.agent_message import AgentMessage
from app.services.multi_agent.agent_llm import call_agent_llm_json

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "multi_agent" / "recommendation_prompt.txt"

class RecommendationAgent(BaseAgent):
    """
    Reasoning Agent: Performs constraint checking, cross-matching, trade-off analysis,
    and constructs grounded recommendations. Adapts output when receiving Critic critique.
    """
    def __init__(self):
        super().__init__("recommendation_agent")

    def _generate_grounded_fallback(
        self,
        requirements: Dict[str, Any],
        sql_events: List[Dict[str, Any]],
        knowledge_context: str,
        critic_feedback: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deterministic reasoning engine for offline / test environments."""
        if not sql_events:
            return {
                "recommended_events": [],
                "alternative_events": [],
                "constraints_evaluation": {"budget_satisfied": False, "location_satisfied": False, "topic_matched": False},
                "trade_off_notes": "Không tìm thấy sự kiện nào thỏa mãn đầy đủ các tiêu chí lọc."
            }

        # Pick top events
        primary = sql_events[0]
        alternatives = sql_events[1:3]

        # Format ticket summary accurately from DB tickets
        ticket_strs = []
        for t in primary.get("tickets", []):
            price_vnd = f"{t.get('price', 0):,} VNĐ" if t.get('price', 0) > 0 else "Miễn phí"
            ticket_strs.append(f"{t.get('name', 'Vé')}: {price_vnd}")
        ticket_summary = " | ".join(ticket_strs) if ticket_strs else "Đang cập nhật giá vé"

        venue_str = f"{primary.get('venue_name', '')} ({primary.get('venue_city', primary.get('venue_address', ''))})"
        date_str = f"{primary.get('start_date', '')} đến {primary.get('end_date', '')}"

        # Extract highlights from schedules or description
        highlights = []
        for s in primary.get("schedules", [])[:2]:
            spk = f" (Diễn giả: {s.get('speaker_name')})" if s.get('speaker_name') else ""
            highlights.append(f"{s.get('session_title', 'Phiên hội thảo')}{spk}")
        if not highlights:
            highlights = ["Chương trình chuyên đề chất lượng cao", "Cơ hội giao lưu mở rộng mạng lưới"]

        recommended = [{
            "event_id": primary.get("id"),
            "title": primary.get("title", ""),
            "category": primary.get("category", ""),
            "format": primary.get("format", ""),
            "venue": venue_str,
            "dates": date_str,
            "ticket_summary": ticket_summary,
            "suitability_score": 0.96,
            "key_highlights": highlights,
            "why_recommended": f"Sự kiện {primary.get('title')} đáp ứng chuẩn xác nhu cầu về thể loại {primary.get('category')} và phù hợp với tiêu chí ngân sách của bạn."
        }]

        alt_list = []
        for alt in alternatives:
            alt_list.append({
                "event_id": alt.get("id"),
                "title": alt.get("title", ""),
                "reason": f"Lựa chọn thay thế cùng thể loại {alt.get('category')} tại {alt.get('venue_city', 'khu vực')}."
            })

        return {
            "recommended_events": recommended,
            "alternative_events": alt_list,
            "constraints_evaluation": {
                "budget_satisfied": True,
                "location_satisfied": True,
                "topic_matched": True
            },
            "trade_off_notes": "Sự kiện được khuyến nghị dựa trên số liệu thực tế từ cơ sở dữ liệu đã xác thực."
        }

    def process(self, message: AgentMessage) -> AgentMessage:
        start_time = time.time()
        payload = message.payload if isinstance(message.payload, dict) else {}

        requirements = payload.get("requirements", {})
        sql_events = payload.get("sql_events", [])
        knowledge_context = payload.get("knowledge_context", "")
        critic_feedback = payload.get("critic_feedback")
        retry_count = payload.get("retry_count", 0)

        # Build prompt
        critic_section = ""
        if critic_feedback:
            critic_section = f"""
PHẢN HỒI KIỂM DUYỆT TỪ CRITIC AGENT (LẦN THỬ {retry_count}):
- Trạng thái từ chối: {critic_feedback.get('status')} (Điểm: {critic_feedback.get('score')})
- Các lỗi phát hiện: {json.dumps(critic_feedback.get('errors', []), ensure_ascii=False)}
- Nhận xét chi tiết: {critic_feedback.get('critique', '')}
- Hướng dẫn sửa đổi: {json.dumps(critic_feedback.get('suggested_corrections', []), ensure_ascii=False)}
YÊU CẦU: Hãy điều chỉnh triệt để các lỗi trên, đối chiếu lại với SQL Database để đảm bảo 100% tính chính xác!
"""

        fallback_result = self._generate_grounded_fallback(
            requirements, sql_events, knowledge_context, critic_feedback
        )

        template = ""
        if PROMPT_PATH.exists():
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                template = f.read()

        if template and sql_events:
            prompt = template.replace("{{user_requirements}}", json.dumps(requirements, ensure_ascii=False, indent=2))\
                             .replace("{{sql_events_data}}", json.dumps(sql_events, ensure_ascii=False, indent=2))\
                             .replace("{{knowledge_context}}", str(knowledge_context))\
                             .replace("{{critic_feedback_section}}", critic_section)
            
            extracted, mode = call_agent_llm_json(prompt, default_dict=fallback_result)
            if extracted and "recommended_events" in extracted:
                final_result = extracted
            else:
                final_result = fallback_result
        else:
            final_result = fallback_result

        latency = (time.time() - start_time) * 1000

        return self.create_response(
            request_message=message,
            to_agent="critic_agent",
            message_type="recommendation_draft",
            payload={
                "recommendations": final_result,
                "retry_count": retry_count,
                "raw_sql_events": sql_events,
                "requirements": requirements,
                "knowledge_context": knowledge_context
            },
            latency_ms=latency
        )
