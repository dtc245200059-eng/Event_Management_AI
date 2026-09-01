"""
AI Blueprint exposing REST API endpoints for RAG Chatbot, Content Generation, Recommendations, Predictive, and Sentiment Analysis.
"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from app.extensions import db
from app.models import AIChatHistory, Event
from app.services.gemini_service import check_rate_limit, call_gemini
from app.services.rag_service import answer_event_query, load_prompt_template
from app.services.recommendation_service import get_personalized_recommendations
from app.services.predictive_service import predict_event_attendance
from app.services.sentiment_service import analyze_event_feedback_sentiment

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/workspace')
def chat_workspace():
    """Giao diện Chatbot AI toàn màn hình chuyên dụng (Dedicated Full-page AI Workspace)."""
    events = Event.query.filter(Event.status.in_(['published', 'ongoing'])).order_by(Event.start_date.asc()).all()
    selected_event_id = request.args.get('event_id', type=int)
    
    recent_chats = []
    if current_user.is_authenticated:
        recent_chats = AIChatHistory.query.filter_by(user_id=current_user.id).order_by(AIChatHistory.created_at.desc()).limit(10).all()
        
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
    Receives user query, retrieves relevant DB context, calls Gemini or Fallback Mock,
    and returns rich Markdown answer.
    """
    data = request.get_json() or {}
    user_message = str(data.get('message', '')).strip()
    event_id = data.get('event_id')

    if not user_message:
        return jsonify({
            'success': False,
            'message': 'Vui lòng nhập nội dung câu hỏi.'
        }), 400

    # Rate limiting by IP or User ID
    client_id = f"user_{current_user.id}" if current_user.is_authenticated else f"ip_{request.remote_addr}"
    if not check_rate_limit(client_id, limit_per_minute=25):
        return jsonify({
            'success': False,
            'message': 'Bạn đang gửi quá nhiều yêu cầu. Vui lòng đợi 1 phút trước khi hỏi tiếp nhé!'
        }), 429

    # RAG Execution
    ai_response, mode, latency_ms = answer_event_query(user_message, event_id=event_id)

    # Save to Chat History Audit
    user_id = current_user.id if current_user.is_authenticated else None
    log_entry = AIChatHistory(
        user_id=user_id,
        event_id=event_id,
        chat_type='rag_chat',
        user_message=user_message,
        ai_response=ai_response,
        model_name='gemini-2.0-flash',
        response_mode=mode,
        latency_ms=latency_ms
    )
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({
        'success': True,
        'response': ai_response,
        'mode': mode,
        'latency_ms': latency_ms
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
