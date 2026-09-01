"""
Recommendation Service: Content-Based Filtering using TF-IDF and Cosine Similarity.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Event, Attendee

def get_personalized_recommendations(attendee_id=None, user_interests=None, top_n=3):
    """
    Tính toán độ tương đồng giữa sở thích của Attendee và nội dung/tags/category của sự kiện
    để xếp hạng Top-N sự kiện phù hợp nhất.
    """
    events = Event.query.filter_by(status='published').all()
    if not events:
        return []

    # 1. Determine query interest text
    interest_text = ""
    if attendee_id:
        attendee = Attendee.query.get(attendee_id)
        if attendee and attendee.interests:
            interest_text = attendee.interests
    if not interest_text and user_interests:
        interest_text = user_interests

    if not interest_text:
        # Default: return newest/upcoming events
        return [{'event': e, 'score': 1.0, 'reason': 'Sự kiện nổi bật sắp diễn ra'} for e in events[:top_n]]

    # 2. Build Event Corpus
    corpus = []
    event_list = []
    for evt in events:
        doc = f"{evt.title} {evt.category} {evt.description or ''} {evt.tags or ''}"
        corpus.append(doc)
        event_list.append(evt)

    # Add user interest as the last document
    corpus.append(interest_text)

    try:
        vectorizer = TfidfVectorizer(stop_words=None)
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Cosine similarity between user vector (last row) and all event vectors
        user_vector = tfidf_matrix[-1]
        event_vectors = tfidf_matrix[:-1]

        similarities = cosine_similarity(user_vector, event_vectors)[0]

        # Rank events
        ranked_indices = similarities.argsort()[::-1]

        recommendations = []
        for idx in ranked_indices[:top_n]:
            score = float(similarities[idx])
            evt = event_list[idx]
            match_pct = int(min(99, max(65, score * 100 + 40))) if score > 0 else 70
            recommendations.append({
                'event': evt,
                'score': score,
                'match_percentage': match_pct,
                'reason': f"Phù hợp với chủ đề '{evt.category}' và từ khóa quan tâm của bạn."
            })

        return recommendations

    except Exception as e:
        print(f"[RECOMMENDATION WARNING] TF-IDF failed: {e}. Fallback to basic match.")
        return [{'event': e, 'score': 0.8, 'match_percentage': 85, 'reason': 'Sự kiện được đề xuất cho bạn'} for e in events[:top_n]]
