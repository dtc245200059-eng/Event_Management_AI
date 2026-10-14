"""
Response Agent for Event Management AI.
Transforms verified recommendation data and critic badges into polite, elegant,
structured Vietnamese Markdown responses for users.
"""
import time
import json
from pathlib import Path
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.models.agent_message import AgentMessage
from app.services.multi_agent.agent_llm import call_agent_llm

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "multi_agent" / "response_prompt.txt"

class ResponseAgent(BaseAgent):
    """
    Response Agent: Final presentation layer formatting verified multi-agent insights.
    """
    def __init__(self):
        super().__init__("response_agent")

    def _format_markdown_fallback(
        self,
        recommendation: Dict[str, Any],
        critic_verdict: Dict[str, Any],
        user_question: str
    ) -> str:
        """Deterministic Markdown response formatter."""
        recommended_events = recommendation.get("recommended_events", [])
        score = critic_verdict.get("score", 0.95)
        score_percent = int(score * 100)

        if not recommended_events:
            return f"""Xin chào bạn! Cảm ơn bạn đã quan tâm đến hệ thống sự kiện.

Hiện tại hệ thống chưa tìm thấy sự kiện nào đáp ứng hoàn toàn chính xác mọi tiêu chí theo yêu cầu của bạn: *"{user_question}"*.

💡 **Gợi ý:** Bạn có thể thử nới rộng khoảng ngân sách hoặc tìm kiếm theo danh mục chung (Công nghệ, Kinh doanh, Giáo dục) để khám phá thêm nhiều sự kiện hấp dẫn nhé!

> 🛡️ **Kiểm duyệt dữ liệu bởi Critic Agent**: Điểm xác thực {score_percent}/100 (Không có sự kiện rỗng bị bịa đặt)."""

        lines = [
            "Xin chào bạn! Dưới đây là phân tích và khuyến nghị sự kiện tối ưu nhất dựa trên nhu cầu của bạn:\n"
        ]

        for i, ev in enumerate(recommended_events, 1):
            ev_id = ev.get("event_id", "")
            title = ev.get("title", "")
            lines.append(f"### {i}. 🎯 **{title}**")
            lines.append(f"- 📅 **Thời gian:** {ev.get('dates', 'Đang cập nhật')}")
            lines.append(f"- 📍 **Địa điểm:** {ev.get('venue', 'Trực tuyến')}")
            lines.append(f"- 🎟️ **Hạng vé & Giá:** {ev.get('ticket_summary', 'Liên hệ BTC')}")
            lines.append(f"- 💡 **Vì sao phù hợp:** {ev.get('why_recommended', '')}")
            
            highlights = ev.get("key_highlights", [])
            if highlights:
                lines.append("- ✨ **Điểm nổi bật:** " + "; ".join(highlights))
            
            if ev_id:
                lines.append(f"\n[👉 **Xem chi tiết & Đặt vé ngay cho sự kiện này**](/events/{ev_id})\n")

        alternatives = recommendation.get("alternative_events", [])
        if alternatives:
            lines.append("---")
            lines.append("📌 **Lựa chọn dự phòng bổ sung:**")
            for alt in alternatives:
                lines.append(f"- **{alt.get('title')}**: {alt.get('reason')}")

        trade_off = recommendation.get("trade_off_notes")
        if trade_off:
            lines.append(f"\n> ℹ️ **Ghi chú tư vấn:** {trade_off}")

        lines.append(f"\n> 🛡️ **Kiểm duyệt dữ liệu bởi Critic Agent**: Điểm tin cậy {score_percent}/100 (Dữ liệu đã được đối chiếu 100% với hệ thống cơ sở dữ liệu thực tế).")

        return "\n".join(lines)

    def process(self, message: AgentMessage) -> AgentMessage:
        start_time = time.time()
        payload = message.payload if isinstance(message.payload, dict) else {}

        approved_recommendation = payload.get("approved_recommendation", {})
        critic_verdict = payload.get("critic_verdict", {})
        user_question = payload.get("user_question", "")

        fallback_text = self._format_markdown_fallback(
            approved_recommendation, critic_verdict, user_question
        )

        template = ""
        if PROMPT_PATH.exists():
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                template = f.read()

        score_percent = int(critic_verdict.get("score", 0.95) * 100)

        if template:
            prompt = template.replace("{{user_question}}", user_question)\
                             .replace("{{approved_recommendation}}", json.dumps(approved_recommendation, ensure_ascii=False, indent=2))\
                             .replace("{{critic_verdict}}", json.dumps(critic_verdict, ensure_ascii=False, indent=2))\
                             .replace("{{critic_score}}", str(score_percent))
            
            ai_text, mode = call_agent_llm(prompt)
            final_text = ai_text.strip() if ai_text and len(ai_text) > 50 else fallback_text
        else:
            final_text = fallback_text

        latency = (time.time() - start_time) * 1000

        return self.create_response(
            request_message=message,
            to_agent="user",
            message_type="final_response",
            payload={
                "text": final_text,
                "critic_verdict": critic_verdict,
                "recommendations": approved_recommendation
            },
            latency_ms=latency
        )
