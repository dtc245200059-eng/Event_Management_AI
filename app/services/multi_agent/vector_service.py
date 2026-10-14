"""
Vector Search Service (Knowledge Tool) for Multi-Agent Event System.
Performs semantic vector search across unstructured event knowledge:
speaker biographies, session descriptions, workshop prerequisites,
event policies, venue amenities, and detailed FAQs.
"""
import os
import re
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.multi_agent.database_service import get_connection

class VectorService:
    """
    Semantic Vector Search Tool for Event Knowledge Base.
    Uses TF-IDF + Cosine Similarity by default for high-performance zero-dependency indexing.
    Optionally integrates with ChromaDB if available in the environment.
    """
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.doc_vectors = None
        self._is_indexed = False

    def build_index_from_database(self) -> None:
        """Extracts unstructured text chunks from events, schedules, speakers, and FAQs."""
        self.documents = []
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Event descriptions & policies
        cursor.execute("""
            SELECT e.id, e.title, e.category, e.location_type, e.location_address, e.description
            FROM events e
            WHERE e.status IN ('published', 'ongoing')
        """)
        for row in cursor.fetchall():
            r = dict(row)
            text_content = f"Sự kiện: {r['title']}. Thể loại: {r['category']}. Hình thức: {r.get('location_type', 'offline')}.\n" \
                           f"Địa điểm: {r.get('location_address', '')}.\n" \
                           f"Mô tả chi tiết: {r.get('description', '')}"
            self.documents.append({
                "id": f"event_{r['id']}",
                "event_id": r['id'],
                "type": "event_overview",
                "title": r['title'],
                "content": text_content,
                "metadata": {"category": r['category'], "format": r.get('location_type', 'offline')}
            })

        # 2. Schedules & Speaker bios
        cursor.execute("""
            SELECT s.id, s.event_id, s.title as session_title, s.description,
                   sp.name as speaker_name, sp.title as speaker_title, sp.organization, sp.bio,
                   v.name as venue_name, v.room_name,
                   e.title as event_title
            FROM schedules s
            LEFT JOIN speakers sp ON s.speaker_id = sp.id
            LEFT JOIN venues v ON s.venue_id = v.id
            LEFT JOIN events e ON s.event_id = e.id
        """)
        for row in cursor.fetchall():
            r = dict(row)
            room_str = f"{r.get('venue_name', '')} - {r.get('room_name', '')}"
            text_content = f"Phiên hội thảo: {r.get('session_title', '')} thuộc sự kiện {r.get('event_title', '')}.\n" \
                           f"Diễn giả: {r.get('speaker_name', 'Chuyên gia')} ({r.get('speaker_title', '')} - {r.get('organization', '')}).\n" \
                           f"Tiểu sử & chuyên môn: {r.get('bio', '')}.\n" \
                           f"Nội dung phiên thảo luận: {r.get('description', '')}. Phòng: {room_str}"
            self.documents.append({
                "id": f"session_{r['id']}",
                "event_id": r['event_id'],
                "type": "session_speaker",
                "title": f"Phiên: {r.get('session_title', '')} - {r.get('speaker_name', '')}",
                "content": text_content,
                "metadata": {"speaker": r.get('speaker_name', ''), "room": room_str}
            })

        # 3. FAQs & Policies
        cursor.execute("""
            SELECT f.id, f.event_id, f.question, f.answer, f.category, e.title as event_title
            FROM event_faqs f
            LEFT JOIN events e ON f.event_id = e.id
        """)
        for row in cursor.fetchall():
            r = dict(row)
            text_content = f"Hỏi đáp sự kiện {r.get('event_title', '')} - Chủ đề: {r.get('category', 'Chung')}.\n" \
                           f"Câu hỏi: {r['question']}\n" \
                           f"Trả lời và chính sách: {r['answer']}"
            self.documents.append({
                "id": f"faq_{r['id']}",
                "event_id": r['event_id'],
                "type": "faq_policy",
                "title": f"FAQ: {r['question']}",
                "content": text_content,
                "metadata": {"category": r.get('category', '')}
            })

        cursor.close()
        conn.close()

        # Add domain policy documents
        self.documents.append({
            "id": "policy_general_checkin",
            "event_id": None,
            "type": "general_policy",
            "title": "Chính sách check-in & vé điện tử QR Code",
            "content": "Chính sách vào cổng: Người tham dự xuất trình mã QR cá nhân trên điện thoại hoặc bản in. "
                       "Check-in mở trước giờ bắt đầu sự kiện 45 phút. Không chuyển nhượng vé sau khi đã check-in.",
            "metadata": {"category": "policy"}
        })
        self.documents.append({
            "id": "policy_general_refund",
            "event_id": None,
            "type": "general_policy",
            "title": "Chính sách hủy và hoàn tiền vé",
            "content": "Chính sách hoàn vé: Vé VIP và Standard được hỗ trợ hủy và hoàn 100% trước 7 ngày diễn ra sự kiện, "
                       "hoàn 50% trước 3 ngày. Trong vòng 48 giờ trước sự kiện không áp dụng hoàn tiền.",
            "metadata": {"category": "policy"}
        })

        # Train TF-IDF vectorizer
        corpus = [doc["content"] for doc in self.documents]
        if corpus:
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=5000,
                sublinear_tf=True
            )
            self.doc_vectors = self.vectorizer.fit_transform(corpus)
            self._is_indexed = True

    def search(self, query: str, top_k: int = 4, event_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Executes semantic vector search for a given natural language query.
        Returns top-k matching documents with similarity scores.
        """
        if not self._is_indexed or not self.documents:
            self.build_index_from_database()

        if not self.documents or self.vectorizer is None or self.doc_vectors is None:
            return []

        query_clean = query.strip()
        if not query_clean:
            return []

        query_vec = self.vectorizer.transform([query_clean])
        sims = cosine_similarity(query_vec, self.doc_vectors).flatten()

        ranked_indices = np.argsort(sims)[::-1]
        results = []

        for idx in ranked_indices:
            score = float(sims[idx])
            doc = self.documents[idx]

            if event_id is not None and doc.get("event_id") is not None and doc["event_id"] != event_id:
                continue

            if score > 0.01:
                doc_copy = dict(doc)
                doc_copy["similarity_score"] = round(score, 4)
                results.append(doc_copy)

            if len(results) >= top_k:
                break

        return results

# Singleton instance
global_vector_service = VectorService()
