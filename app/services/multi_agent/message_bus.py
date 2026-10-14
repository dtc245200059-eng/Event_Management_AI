"""
Message Bus & Execution Trace Logger for Multi-Agent Event System.
Maintains in-memory trace history of all agent messages for inspection and auditing.
"""
from typing import Dict, List, Any, Optional
from collections import defaultdict
import threading
from app.models.agent_message import AgentMessage

class MessageBus:
    """Central message bus and audit logger for agent communications."""
    def __init__(self):
        self._traces: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._lock = threading.Lock()

    def record_message(self, message: AgentMessage) -> None:
        """Records an AgentMessage into the trace log."""
        with self._lock:
            self._traces[message.task_id].append(message.to_dict())

    def get_trace(self, task_id: str) -> List[Dict[str, Any]]:
        """Retrieves chronological execution trace for a given task ID."""
        with self._lock:
            return list(self._traces.get(task_id, []))

    def clear_task(self, task_id: str) -> None:
        """Cleans up memory for a completed task trace."""
        with self._lock:
            if task_id in self._traces:
                del self._traces[task_id]

    def get_recent_task_ids(self, limit: int = 20) -> List[str]:
        """Lists most recent task IDs."""
        with self._lock:
            keys = list(self._traces.keys())
            return keys[-limit:]

# Singleton instance
global_message_bus = MessageBus()
