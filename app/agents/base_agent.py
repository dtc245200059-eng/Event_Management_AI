"""
Base Agent Abstract Class for Multi-Agent Event System.
Enforces a consistent interface across all 7 specialized agents.
"""
from abc import ABC, abstractmethod
import time
from typing import Any, Optional
from app.models.agent_message import AgentMessage

class BaseAgent(ABC):
    """
    Abstract Base Class for all agents.
    Every agent must implement the process() method receiving and returning an AgentMessage.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process(self, message: AgentMessage) -> AgentMessage:
        """
        Process incoming AgentMessage and produce a response AgentMessage.
        Must be implemented by concrete subclasses.
        """
        pass

    def create_response(
        self,
        request_message: AgentMessage,
        to_agent: str,
        message_type: str,
        payload: Any,
        status: str = "success",
        error: Optional[str] = None,
        latency_ms: Optional[float] = None
    ) -> AgentMessage:
        """Helper to create a properly addressed downstream AgentMessage."""
        meta = dict(request_message.metadata or {})
        if latency_ms is not None:
            meta[f"{self.name}_latency_ms"] = round(latency_ms, 2)

        return AgentMessage(
            task_id=request_message.task_id,
            from_agent=self.name,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            status=status,
            error=error,
            metadata=meta
        )
