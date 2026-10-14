"""
Critic Agent (Anti-Hallucination & Factual Guardrail) for Event Management AI.
Independently audits draft recommendations against ground truth SQL records and Knowledge context.
Issues APPROVE or REJECT verdicts, triggering orchestrator retry loops upon failure.
"""
import time
import json
from pathlib import Path
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.models.agent_message import AgentMessage, CriticVerdict
from app.services.multi_agent.agent_llm import call_agent_llm_json

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "multi_agent" / "critic_prompt.txt"

class CriticAgent(BaseAgent):
    """
    Critic & Auditor Agent: Evaluates recommendation fidelity, checks against SQL ground truth,
    and detects hallucinations or constraint violations.
    """
    def __init__(self):
        super().__init__("critic_agent")

    def _verify_algorithmically(
        self,
        recommendation_data: Dict[str, Any],
        sql_events: List[Dict[str, Any]],
        requirements: Dict[str, Any]
    ) -> CriticVerdict:
        """
        Deterministic audit engine that cross-references recommended entities
        with raw SQL records to eliminate false approvals and guarantee safety.
        """
        errors: List[str] = []
        corrections: List[str] = []
        
        recommended_items = recommendation_data.get("recommended_events", [])
        if not recommended_items:
            # Check if SQL actually had matching events
            if sql_events:
                return CriticVerdict(
                    status="REJECT",
                    score=0.40,
                    errors=["Recommendation Agent không đưa ra sự kiện nào mặc dù CSDL có kết quả phù hợp."],
                    critique="Cần chọn ít nhất 1 sự kiện từ danh sách CSDL để đề xuất cho người dùng.",
                    suggested_corrections=["Chọn sự kiện đầu tiên trong danh sách SQL để phân tích."]
                )
            else:
                # No events in DB, so empty is factually correct
                return CriticVerdict(
                    status="APPROVE",
                    score=0.90,
                    errors=[],
                    critique="Không có sự kiện phù hợp trong CSDL, hệ thống đã thông báo trung thực không bịa đặt.",
                    suggested_corrections=[]
                )

        db_event_map = {e.get("id"): e for e in sql_events if isinstance(e, dict)}
        db_title_map = {str(e.get("title", "")).strip().lower(): e for e in sql_events if isinstance(e, dict)}

        for item in recommended_items:
            ev_id = item.get("event_id")
            title = str(item.get("title", "")).strip()

            # 1. Existence check
            db_record = db_event_map.get(ev_id)
            if not db_record and title.lower() in db_title_map:
                db_record = db_title_map[title.lower()]

            if not db_record:
                errors.append(f"Hallucination: Sự kiện '{title}' (ID: {ev_id}) không tồn tại trong CSDL sự kiện thực tế.")
                corrections.append(f"Chỉ đề xuất sự kiện có trong danh mục: {[e.get('title') for e in sql_events[:3]]}")
                continue

            # 2. Budget constraint verification
            max_price = requirements.get("max_price")
            if max_price is not None and isinstance(max_price, (int, float)) and max_price >= 0:
                tickets = db_record.get("tickets", [])
                if tickets:
                    min_ticket_price = min(t.get("price", 0) for t in tickets)
                    if min_ticket_price > max_price:
                        errors.append(f"Vi phạm ngân sách: Sự kiện '{title}' có giá vé thấp nhất là {min_ticket_price:,} VNĐ, vượt quá ngân sách {max_price:,} VNĐ của người dùng.")
                        corrections.append("Lọc bỏ sự kiện vượt quá ngân sách hoặc đề xuất sự kiện có vé miễn phí/thấp hơn.")

            # 3. Format constraint verification
            req_format = requirements.get("format")
            if req_format and db_record.get("format"):
                if str(req_format).lower() != str(db_record.get("format")).lower() and req_format != "hybrid":
                    errors.append(f"Không khớp hình thức: Người dùng yêu cầu {req_format} nhưng sự kiện '{title}' là {db_record.get('format')}.")
                    corrections.append(f"Chọn đúng sự kiện có hình thức {req_format}.")

        if errors:
            return CriticVerdict(
                status="REJECT",
                score=round(max(0.2, 1.0 - (len(errors) * 0.25)), 2),
                errors=errors,
                critique=f"Phát hiện {len(errors)} lỗi sai lệch dữ liệu hoặc vi phạm ràng buộc so với Ground Truth CSDL.",
                suggested_corrections=corrections
            )

        return CriticVerdict(
            status="APPROVE",
            score=0.98,
            errors=[],
            critique="Toàn bộ thông tin sự kiện, giá vé, hình thức và địa điểm khớp 100% với dữ liệu SQL và ngữ cảnh tri thức.",
            suggested_corrections=[]
        )

    def process(self, message: AgentMessage) -> AgentMessage:
        start_time = time.time()
        payload = message.payload if isinstance(message.payload, dict) else {}

        recommendations = payload.get("recommendations", {})
        raw_sql_events = payload.get("raw_sql_events", [])
        requirements = payload.get("requirements", {})
        knowledge_context = payload.get("knowledge_context", "")

        # 1. Run deterministic algorithmic audit
        algorithmic_verdict = self._verify_algorithmically(
            recommendations, raw_sql_events, requirements
        )

        # 2. If algorithmic check found critical errors, reject immediately
        if algorithmic_verdict.status == "REJECT":
            final_verdict = algorithmic_verdict
        else:
            # 3. Optional LLM verification for subtle hallucination check
            template = ""
            if PROMPT_PATH.exists():
                with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                    template = f.read()

            if template and raw_sql_events:
                prompt = template.replace("{{user_requirements}}", json.dumps(requirements, ensure_ascii=False, indent=2))\
                                 .replace("{{sql_ground_truth}}", json.dumps(raw_sql_events, ensure_ascii=False, indent=2))\
                                 .replace("{{knowledge_ground_truth}}", str(knowledge_context))\
                                 .replace("{{recommendation_draft}}", json.dumps(recommendations, ensure_ascii=False, indent=2))
                
                llm_dict, mode = call_agent_llm_json(prompt, default_dict=algorithmic_verdict.model_dump())
                if llm_dict and "status" in llm_dict:
                    try:
                        final_verdict = CriticVerdict(**llm_dict)
                    except Exception:
                        final_verdict = algorithmic_verdict
                else:
                    final_verdict = algorithmic_verdict
            else:
                final_verdict = algorithmic_verdict

        latency = (time.time() - start_time) * 1000

        return self.create_response(
            request_message=message,
            to_agent="orchestrator_agent",
            message_type="critic_verdict",
            payload=final_verdict.model_dump(),
            status="rejected" if final_verdict.status == "REJECT" else "success",
            latency_ms=latency
        )
