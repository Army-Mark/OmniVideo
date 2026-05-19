from api.endpoints.parse import router as parse_router
from api.endpoints.download import router as download_router
from api.endpoints.ai import router as ai_router
from api.endpoints.user import router as user_router

__all__ = ["parse_router", "download_router", "ai_router", "user_router"]
