"""Root services alias for message_bus."""
from app.services.multi_agent.message_bus import MessageBus, global_message_bus

__all__ = ['MessageBus', 'global_message_bus']
