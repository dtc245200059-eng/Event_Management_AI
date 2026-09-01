"""
RAG Service: Structured Context Retrieval from SQLite Database + Prompt Grounding.
"""
import os
import time
from flask import current_app
from app.models import Event, Speaker, Venue, Schedule, Ticket
from app.services.gemini_service import call_gemini

def load_prompt_template(filename):
    """Đọc prompt template từ thư mục app/prompts/."""
    prompts_dir = os.path.join(current_app.root_path, 'prompts')
    filepath = os.path.join(prompts_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def build_retrieved_context(query_text="", target_event_id=None):
    """
    Truy xuất có cấu trúc dữ liệu sự kiện, lịch trình, diễn giả, vé từ CSDL SQLite
    để tạo thành Grounded Context chèn vào Prompt.
    """
    context_chunks = []

    # 1. Truy xuất Sự kiện
    if target_event_id:
        events = Event.query.filter_by(id=target_event_id).all()
    else:
        events = Event.query.filter(Event.status.in_(['published', 'ongoing'])).limit(5).all()

    for evt in events:
        evt_info = f"[SỰ KIỆN]: {evt.title} (Mã: {evt.event_code})\n"
        evt_info += f"- Chủ đề/Danh mục: {evt.category}\n"
        evt_info += f"- Thời gian: {evt.start_date.strftime('%H:%M %d/%m/%Y')} đến {evt.end_date.strftime('%H:%M %d/%m/%Y')}\n"
        evt_info += f"- Hình thức/Địa điểm: {evt.location_type.upper()} - {evt.location_address or 'Online'}\n"
        evt_info += f"- Mô tả: {evt.description}\n"
        
        # Tickets
        tickets = evt.tickets.all()
        if tickets:
            evt_info += "- Các loại vé:\n"
            for t in tickets:
                price_str = "Miễn phí" if t.price == 0 else f"{t.price:,.0f} VNĐ"
                status_str = "Còn vé" if t.is_available else "Hết vé"
                evt_info += f"  + {t.name} ({t.ticket_type.upper()}): {price_str} | Số lượng còn: {t.remaining_quota}/{t.quota} ({status_str})\n"

        # Schedules & Speakers
        schedules = evt.schedules.order_by(Schedule.start_at.asc()).all()
        if schedules:
            evt_info += "- Lịch trình các phiên họp (Agenda):\n"
            for s in schedules:
                spk_name = s.speaker.name if s.speaker else "Ban tổ chức"
                spk_org = f" ({s.speaker.organization})" if s.speaker and s.speaker.organization else ""
                vne_name = s.venue.name if s.venue else "Hội trường chính"
                evt_info += f"  + [{s.start_at.strftime('%H:%M')} - {s.end_at.strftime('%H:%M')}]: {s.title}\n"
                evt_info += f"    Diễn giả: {spk_name}{spk_org} | Địa điểm: {vne_name}\n"
                if s.description:
                    evt_info += f"    Nội dung: {s.description}\n"

        context_chunks.append(evt_info)

    # 2. Thông tin Diễn giả chung
    speakers = Speaker.query.limit(4).all()
    if speakers:
        spk_chunk = "[DANH SÁCH DIỄN GIẢ TIÊU BIỂU]:\n"
        for spk in speakers:
            spk_chunk += f"- {spk.name} ({spk.title or 'Chuyên gia'}, {spk.organization or ''}): {spk.bio or ''}\n"
        context_chunks.append(spk_chunk)

    return "\n\n".join(context_chunks)

def answer_event_query(user_message, event_id=None):
    """
    RAG Pipeline hoàn chỉnh:
    Query -> Retrieve DB -> Format Context -> System Prompt Template -> LLM / Fallback.
    """
    start_time = time.time()
    
    # 1. Retrieve structured context
    context = build_retrieved_context(query_text=user_message, target_event_id=event_id)
    
    # 2. Load System Prompt Template
    system_template = load_prompt_template('chatbot_system.txt')
    if "{{retrieved_context}}" in system_template:
        system_instruction = system_template.replace("{{retrieved_context}}", context)
    else:
        system_instruction = f"{system_template}\n\n[CONTEXT DỮ LIỆU]:\n{context}"

    # 3. User Prompt
    prompt = f"Câu hỏi của người dùng: {user_message}"

    # 4. Call LLM
    response_text, mode = call_gemini(prompt=prompt, system_instruction=system_instruction)
    latency_ms = int((time.time() - start_time) * 1000)

    return response_text, mode, latency_ms
