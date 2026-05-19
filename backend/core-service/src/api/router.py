from fastapi import APIRouter

from api.endpoints import parse, download, ai, user

api_router = APIRouter()

api_router.include_router(parse.router, prefix="/parse", tags=["解析"])
api_router.include_router(download.router, prefix="/download", tags=["下载"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI分析"])
api_router.include_router(user.router, prefix="/user", tags=["用户"])
