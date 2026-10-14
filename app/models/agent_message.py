"""
Structured Message Protocol for Multi-Agent System.
Defines AgentMessage and CriticVerdict adhering to the Agentic SDLC architecture.
"""
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict, List
from datetime import datetime, timezone
import uuid

class CriticVerdict(BaseModel):
    """Structured review verdict issued by Critic Agent."""
    status: str = Field(default="APPROVE", description="'APPROVE' or 'REJECT'")
    score: float = Field(default=1.0, ge=0.0, le=1.0, description="Factual and constraint adherence score")
    errors: List[str] = Field(default_factory=list, description="Specific factual or constraint errors identified")
    critique: str = Field(default="", description="Detailed qualitative feedback for the reasoning agent")
    suggested_corrections: List[str] = Field(default_factory=list, description="Actionable correction hints")

class AgentMessage(BaseModel):
    """
    Structured Message for Agent-to-Agent communication.
    Guarantees strict type safety, trace tracking, and structured payloads.
    """
    task_id: str = Field(default_factory=lambda: f"TASK-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}")
    from_agent: str = Field(..., description="Name of sender agent, e.g. orchestrator_agent, requirement_agent")
    to_agent: str = Field(..., description="Name of target agent, e.g. retrieval_agent, response_agent")
    message_type: str = Field(..., description="Semantic purpose, e.g. user_query, requirements, sql_result, critic_verdict")
    payload: Any = Field(..., description="Structured payload (dict, list, or primitive)")
    status: str = Field(default="success", description="'success', 'retry', 'rejected', or 'error'")
    error: Optional[str] = Field(default=None, description="Error message if execution failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution metadata like latency, timestamp")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Converts model to serializable dictionary."""
        return self.model_dump()
