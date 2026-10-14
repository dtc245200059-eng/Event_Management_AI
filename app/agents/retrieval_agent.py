"""
Retrieval Agent (Database / SQL Tool Agent) for Event Management AI.
Interfaces with relational database via parameterized SQL to fetch verified event records.
"""
import time
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.models.agent_message import AgentMessage
from app.services.multi_agent.database_service import (
    search_events_sql,
    get_event_full_details_sql,
    get_all_events_summary_sql
)

class RetrievalAgent(BaseAgent):
    """
    Database Agent: Executes SQL tool queries to retrieve grounded event data, tickets, and venues.
    """
    def __init__(self):
        super().__init__("retrieval_agent")

    def process(self, message: AgentMessage) -> AgentMessage:
        start_time = time.time()
        criteria = message.payload if isinstance(message.payload, dict) else {}

        # 1. Primary parameterized search
        events = search_events_sql(criteria)

        # 2. Relaxed fallback search if strict search yielded 0 results
        if not events:
            relaxed_criteria = {
                "category": criteria.get("category"),
                "max_price": criteria.get("max_price")
            }
            events = search_events_sql(relaxed_criteria)

        # 3. Last fallback: return active event summary
        if not events:
            events = get_all_events_summary_sql(limit=5)

        # 4. Enrich top candidate events with complete relational details (tickets, schedules, venue)
        detailed_events: List[Dict[str, Any]] = []
        for e in events[:4]:
            full_data = get_event_full_details_sql(e["id"])
            if full_data:
                detailed_events.append(full_data)
            else:
                detailed_events.append(e)

        latency = (time.time() - start_time) * 1000

        return self.create_response(
            request_message=message,
            to_agent="orchestrator_agent",
            message_type="sql_events_result",
            payload={
                "matched_events": detailed_events,
                "total_found": len(events),
                "criteria_used": criteria
            },
            latency_ms=latency
        )
