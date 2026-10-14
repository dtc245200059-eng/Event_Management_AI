"""
Knowledge Agent (Vector Search / RAG Tool Agent) for Event Management AI.
Retrieves unstructured semantic knowledge: speaker bios, agenda specifics, policies, FAQs.
"""
import time
from pathlib import Path
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.models.agent_message import AgentMessage
from app.services.multi_agent.vector_service import global_vector_service
from app.services.multi_agent.agent_llm import call_agent_llm

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "multi_agent" / "knowledge_prompt.txt"

class KnowledgeAgent(BaseAgent):
    """
    RAG & Vector Agent: Performs semantic retrieval on unstructured event documents.
    """
    def __init__(self):
        super().__init__("knowledge_agent")

    def process(self, message: AgentMessage) -> AgentMessage:
        start_time = time.time()
        
        # Determine search query
        query = ""
        event_id = None
        if isinstance(message.payload, dict):
            query = message.payload.get("original_question") or message.payload.get("query", "")
            event_id = message.payload.get("event_id")
            # If query is empty, compose from topics and category
            if not query:
                parts = []
                if message.payload.get("category"):
                    parts.append(str(message.payload["category"]))
                if message.payload.get("topics"):
                    parts.extend(message.payload["topics"])
                if message.payload.get("speaker"):
                    parts.append(str(message.payload["speaker"]))
                query = " ".join(parts)
        elif isinstance(message.payload, str):
            query = message.payload

        # Execute Vector Search
        docs = global_vector_service.search(query=query, top_k=4, event_id=event_id)

        # Prepare formatted context string
        context_snippets = []
        for i, d in enumerate(docs, 1):
            context_snippets.append(f"[{i}] {d.get('title', '')} (Score: {d.get('similarity_score', 0)}):\n{d.get('content', '')}")
        context_str = "\n\n".join(context_snippets) if context_snippets else "Không tìm thấy tài liệu phi cấu trúc bổ sung."

        # Quick synthesis via prompt template if available
        summary = ""
        if PROMPT_PATH.exists() and docs:
            try:
                with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                    template = f.read()
                prompt = template.replace("{{retrieved_documents}}", context_str)\
                                 .replace("{{user_question}}", query)
                text, _ = call_agent_llm(prompt)
                summary = text
            except Exception:
                summary = context_str
        else:
            summary = context_str

        latency = (time.time() - start_time) * 1000

        return self.create_response(
            request_message=message,
            to_agent="orchestrator_agent",
            message_type="vector_knowledge_result",
            payload={
                "documents": docs,
                "context_summary": summary,
                "query": query
            },
            latency_ms=latency
        )
