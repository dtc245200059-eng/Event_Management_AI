"""
AI Blueprint exposing REST API endpoints for RAG Chatbot, Content Generation, Recommendations, Predictive, and Sentiment Analysis.
"""
from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import current_user
from app.extensions import db
from app.models import AIChatHistory, Event
from app.services.gemini_service import check_rate_limit, call_gemini
from app.services.rag_service import answer_event_query, load_prompt_template
from app.services.recommendation_service import get_personalized_recommendations
from app.services.predictive_service import predict_event_attendance
from app.services.sentiment_service import analyze_event_feedback_sentiment, summarize_event_feedback_groups
from app.agents.orchestrator_agent import OrchestratorAgent
from app.models.agent_message import AgentMessage
from app.services.multi_agent.message_bus import global_message_bus
import json
import re

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/workspace')
def chat_workspace():
    """Giao diện Chatbot AI toàn màn hình chuyên dụng (Dedicated Full-page AI Workspace)."""
    events = Event.query.filter(Event.status.in_(['published', 'ongoing'])).order_by(Event.start_date.asc()).all()
    selected_event_id = request.args.get('event_id', type=int)
    
    recent_chats = []
    if current_user.is_authenticated:
        recent_chats = AIChatHistory.query.filter_by(user_id=current_user.id).order_by(AIChatHistory.created_at.desc()).limit(15).all()
        
    return render_template(
        'ai/chat_workspace.html',
        events=events,
        selected_event_id=selected_event_id,
        recent_chats=recent_chats
    )

@ai_bp.route('/chat', methods=['POST'])
def chat():
    """
    RAG Chatbot API Endpoint.
    Receives user query + conversation history, retrieves relevant DB context,
    calls Gemini 3.6 Flash (or Local Grounded Fallback), and returns rich Markdown answer.
    """
    data = request.get_json() or {}
    user_message = str(data.get('message', '')).strip()
    event_id = data.get('event_id')
    history = data.get('history', [])

    if not user_message:
        return jsonify({
            'success': False,
            'message': 'Vui lòng nhập nội dung câu hỏi.'
        }), 400

    # Rate limiting by IP or User ID
    client_id = f"user_{current_user.id}" if current_user.is_authenticated else f"ip_{request.remote_addr}"
    if not check_rate_limit(client_id, limit_per_minute=30):
        return jsonify({
            'success': False,
            'message': 'Bạn đang gửi quá nhiều yêu cầu. Vui lòng đợi 1 phút trước khi hỏi tiếp nhé!'
        }), 429

    try:
        # RAG Execution with multi-turn history
        ai_response, mode, latency_ms = answer_event_query(user_message, event_id=event_id, history=history)

        # Save to Chat History Audit
        try:
            user_id = current_user.id if current_user.is_authenticated else None
            log_entry = AIChatHistory(
                user_id=user_id,
                event_id=event_id,
                chat_type='rag_chat',
                user_message=user_message,
                ai_response=ai_response,
                model_name=current_app.config.get('GEMINI_MODEL', 'gemini-3.6-flash'),
                response_mode=mode,
                latency_ms=latency_ms
            )
            db.session.add(log_entry)
            db.session.commit()
        except Exception as db_err:
            db.session.rollback()

        return jsonify({
            'success': True,
            'response': ai_response,
            'mode': mode,
            'latency_ms': latency_ms
        })
    except Exception as exc:
        db.session.rollback()
        from app.services.gemini_service import generate_comprehensive_response
        fallback_ans = generate_comprehensive_response(user_message)
        return jsonify({
            'success': True,
            'response': fallback_ans,
            'mode': 'mock',
            'latency_ms': 50
        })

@ai_bp.route('/generate-description', methods=['POST'])
def generate_description():
    """
    AI Content Generator for Organizer / Admin Event Creation form.
    """
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    category = data.get('category', '').strip()
    time_info = data.get('time', '').strip()
    location = data.get('location', '').strip()
    highlights = data.get('highlights', '').strip()

    if not title:
        return jsonify({
            'success': False,
            'message': 'Vui lòng nhập tên sự kiện trước khi sinh mô tả.'
        }), 400

    template = load_prompt_template('event_generator.txt')
    prompt = template.replace('{{event_title}}', title)\
                     .replace('{{event_category}}', category or 'Công nghệ & Đổi mới')\
                     .replace('{{event_time}}', time_info or 'Sắp diễn ra')\
                     .replace('{{event_location}}', location or 'Hội trường chính')\
                     .replace('{{event_highlights}}', highlights or 'Chia sẻ kiến thức chuyên sâu và kết nối chuyên gia')

    generated_text, mode = call_gemini(prompt)

    return jsonify({
        'success': True,
        'description': generated_text,
        'mode': mode
    })

@ai_bp.route('/recommendations', methods=['GET'])
def recommendations():
    """
    Personalized Event Recommendations with Horizontal Slider support.
    """
    attendee_id = current_user.attendee_profile.id if (current_user.is_authenticated and current_user.attendee_profile) else None
    interests = request.args.get('interests', '')

    recs = get_personalized_recommendations(attendee_id=attendee_id, user_interests=interests, top_n=8)

    results = []
    for r in recs:
        evt = r['event']
        results.append({
            'id': evt.id,
            'event_code': evt.event_code,
            'title': evt.title,
            'category': evt.category,
            'start_date': evt.start_date.strftime('%H:%M • %d/%m/%Y'),
            'banner_url': evt.banner_url,
            'location_type': evt.location_type,
            'location_address': evt.location_address,
            'match_percentage': r.get('match_percentage', 85),
            'reason': r.get('reason', '')
        })

    return jsonify({
        'success': True,
        'recommendations': results
    })

@ai_bp.route('/predictive/<int:event_id>', methods=['GET'])
def predictive_stats(event_id):
    """
    Predictive Analytics endpoint for Event Dashboard.
    """
    stats = predict_event_attendance(event_id)
    if not stats:
        return jsonify({'success': False, 'message': 'Không tìm thấy sự kiện'}), 404
    return jsonify({'success': True, 'stats': stats})

@ai_bp.route('/sentiment/<int:event_id>', methods=['GET'])
def sentiment_stats(event_id):
    """
    Feedback Sentiment Analysis endpoint.
    """
    stats = analyze_event_feedback_sentiment(event_id)
    return jsonify({'success': True, 'stats': stats})

@ai_bp.route('/generate-notification', methods=['POST'])
def generate_notification():
    """
    AI Notification / Email Content Generator (Requirement 3.2.1 de_tai_09.md).
    Generates tailored email draft (invitation, reminder, thank-you, update)
    strictly based on event info without hallucination or exposing attendee PII.
    """
    data = request.get_json() or {}
    event_id = data.get('event_id')
    notification_type = data.get('notification_type', 'reminder')
    target_audience = data.get('target_audience', 'sinh viên và người tham dự đã đăng ký')

    if not event_id:
        return jsonify({'success': False, 'message': 'Vui lòng chọn sự kiện.'}), 400

    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({'success': False, 'message': 'Không tìm thấy sự kiện.'}), 404

    # Build sanitized event info without attendee PII
    speakers_list = []
    for s in event.schedules:
        if s.speaker and s.speaker.name not in speakers_list:
            speakers_list.append(f"{s.speaker.name} ({s.speaker.title or 'Diễn giả'} - {s.speaker.organization or ''})")

    speakers_str = ", ".join(speakers_list) if speakers_list else "Các chuyên gia và diễn giả khách mời uy tín"
    
    event_info = f"""- Tên sự kiện: {event.title}
- Mã sự kiện: {event.event_code}
- Danh mục: {event.category}
- Thời gian bắt đầu: {event.start_date.strftime('%H:%M ngày %d/%m/%Y')}
- Thời gian kết thúc: {event.end_date.strftime('%H:%M ngày %d/%m/%Y')}
- Hình thức: {event.location_type.upper()}
- Địa điểm / Phòng: {event.location_address or 'Trực tuyến qua Zoom / Google Meet'}
- Diễn giả tiêu biểu: {speakers_str}
- Tóm tắt nội dung: {event.description or 'Chương trình chia sẻ kiến thức chuyên sâu và kết nối cộng đồng.'}"""

    template = load_prompt_template('notification_generator.txt')
    prompt = template.replace('{{event_info}}', event_info)\
                     .replace('{{notification_type}}', notification_type)\
                     .replace('{{target_audience}}', target_audience)

    response_text, mode = call_gemini(prompt)

    try:
        clean_json = re.sub(r'```json\s*|\s*```', '', response_text).strip()
        result = json.loads(clean_json)
        subject = result.get('subject', f"[{notification_type.upper()}] Thông báo về sự kiện {event.title}")
        content = result.get('content', response_text)
    except Exception:
        # Fallback formatting if raw text returned
        subject = f"[Thông báo] {event.title} - Lịch trình và hướng dẫn tham dự"
        content = response_text

    return jsonify({
        'success': True,
        'subject': subject,
        'content': content,
        'mode': mode
    })

@ai_bp.route('/feedback-summary/<int:event_id>', methods=['GET'])
def feedback_summary(event_id):
    """
    AI Feedback Opinion Groups Summarizer endpoint (Requirement 3.2.2 de_tai_09.md).
    Returns grouped opinions (Content & Speakers, Check-in, Venue, Schedule) + Actionable Takeaways.
    """
    summary = summarize_event_feedback_groups(event_id)
    return jsonify(summary)

# =============================================================================
# MULTI-AGENT ADVISORY & DECISION MAKING SYSTEM ENDPOINTS
# =============================================================================

@ai_bp.route('/multi-agent/advisory', methods=['POST'])
def multi_agent_advisory():
    """
    Multi-Agent Event Advisory Endpoint.
    Orchestrates 7 specialized agents (Orchestrator, Requirement, Retrieval SQL,
    Knowledge Vector, Recommendation Reasoning, Critic Reviewer, Response Agent)
    with Critic validation and Retry loops.
    """
    data = request.get_json() or {}
    question = str(data.get('question') or data.get('message', '')).strip()
    max_retries = int(data.get('max_retries', 2))

    if not question:
        return jsonify({
            'success': False,
            'message': 'Vui lòng nhập câu hỏi tư vấn sự kiện.'
        }), 400

    # Rate limiting
    client_id = f"user_{current_user.id}" if current_user.is_authenticated else f"ip_{request.remote_addr}"
    if not check_rate_limit(client_id, limit_per_minute=25):
        return jsonify({
            'success': False,
            'message': 'Bạn đang gửi quá nhiều yêu cầu tư vấn. Vui lòng đợi một lát.'
        }), 429

    try:
        orchestrator = OrchestratorAgent(max_retries=max_retries)
        initial_msg = AgentMessage(
            from_agent="user",
            to_agent="orchestrator_agent",
            message_type="user_inquiry",
            payload={"question": question}
        )
        response_msg = orchestrator.process(initial_msg)
        result_payload = response_msg.payload

        # Audit into AIChatHistory
        try:
            user_id = current_user.id if current_user.is_authenticated else None
            log_entry = AIChatHistory(
                user_id=user_id,
                chat_type='multi_agent_advisory',
                user_message=question,
                ai_response=result_payload.get('answer', ''),
                model_name='Multi-Agent-7-Ensemble',
                response_mode='multi_agent',
                latency_ms=result_payload.get('total_latency_ms', 0)
            )
            db.session.add(log_entry)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return jsonify({
            'success': True,
            'task_id': response_msg.task_id,
            'answer': result_payload.get('answer', ''),
            'critic_verdict': result_payload.get('critic_verdict', {}),
            'retry_count': result_payload.get('retry_count', 0),
            'total_latency_ms': result_payload.get('total_latency_ms', 0),
            'trace': result_payload.get('trace', []),
            'recommendations': result_payload.get('recommendation', {})
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi thực thi quy trình Multi-Agent: {str(e)}'
        }), 500

@ai_bp.route('/multi-agent/trace/<task_id>', methods=['GET'])
def get_multi_agent_trace(task_id):
    """Retrieves step-by-step agent execution trace from the MessageBus for auditing."""
    trace = global_message_bus.get_trace(task_id)
    return jsonify({
        'success': True,
        'task_id': task_id,
        'step_count': len(trace),
        'trace': trace
    })

@ai_bp.route('/multi-agent/benchmark', methods=['POST'])
def run_benchmark_endpoint():
    """Triggers the 10-test-case Single-Agent vs Multi-Agent benchmark evaluation."""
    from app.services.multi_agent.benchmark_service import run_benchmark_suite
    data = request.get_json() or {}
    quick_mode = bool(data.get('quick_mode', True))
    results = run_benchmark_suite(quick_mode=quick_mode)
    return jsonify({
        'success': True,
        'summary': results.get('summary', {}),
        'test_cases': results.get('test_cases', [])
    })

