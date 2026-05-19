from fastapi import APIRouter, HTTPException
from parsers.parser_factory import ParserFactory
from models.schemas import ParseRequest, ParseResponse, VideoInfo

router = APIRouter()


@router.post("/", response_model=ParseResponse)
async def parse_video(request: ParseRequest):
    """解析视频链接"""
    try:
        video_info = await ParserFactory.parse(request.url)

        if not video_info:
            return ParseResponse(
                code=400,
                message="无法解析该链接，请检查链接是否正确或平台是否支持",
                data=None,
            )

        return ParseResponse(
            code=200,
            message="解析成功",
            data=video_info,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")


@router.get("/platforms")
async def get_supported_platforms():
    """获取支持的平台列表"""
    return {
        "code": 200,
        "data": [
            {"id": "douyin", "name": "抖音", "status": "active"},
            {"id": "bilibili", "name": "哔哩哔哩", "status": "active"},
            {"id": "xiaohongshu", "name": "小红书", "status": "active"},
            {"id": "kuaishou", "name": "快手", "status": "coming_soon"},
            {"id": "youtube", "name": "YouTube", "status": "coming_soon"},
            {"id": "pipixia", "name": "皮皮虾", "status": "coming_soon"},
        ],
    }
