"""Root services alias for database_service."""
from app.services.multi_agent.database_service import (
    get_connection,
    search_events_sql,
    get_event_full_details_sql,
    get_all_events_summary_sql
)

__all__ = [
    'get_connection',
    'search_events_sql',
    'get_event_full_details_sql',
    'get_all_events_summary_sql'
]
