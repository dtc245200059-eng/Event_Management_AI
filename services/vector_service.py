"""Root services alias for vector_service."""
from app.services.multi_agent.vector_service import VectorService, global_vector_service

__all__ = ['VectorService', 'global_vector_service']
