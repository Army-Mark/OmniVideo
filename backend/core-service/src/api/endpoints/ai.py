import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from ai.qwen3vl import Qwen3VLAnalyzer
from models.schemas import AIAnalysisResponse

router = APIRouter()
analyzer = Qwen3VLAnalyzer()


@router.post("/analyze", response_model=AIAnalysisResponse)
async def analyze_video(
    video: UploadFile = File(...),
    prompt: str = Form("请描述这个视频的内容"),
    max_frames: int = Form(6),
):
    """分析视频内容"""
    temp_path = None
    try:
        suffix = os.path.splitext(video.filename or "")[1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await video.read()
            tmp.write(content)
            temp_path = tmp.name

        result = await analyzer.analyze_video(temp_path, prompt, max_frames)

        if result.get("success"):
            return AIAnalysisResponse(
                code=200,
                message="分析成功",
                data=result,
            )
        else:
            return AIAnalysisResponse(
                code=400,
                message=result.get("error", "分析失败"),
                data=None,
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post("/summary")
async def generate_summary(video: UploadFile = File(...)):
    """生成视频摘要"""
    temp_path = None
    try:
        suffix = os.path.splitext(video.filename or "")[1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await video.read()
            tmp.write(content)
            temp_path = tmp.name

        result = await analyzer.generate_summary(temp_path)

        if result.get("success"):
            return {"code": 200, "data": result}
        else:
            return {"code": 400, "message": result.get("error", "分析失败")}

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post("/keywords")
async def extract_keywords(video: UploadFile = File(...)):
    """提取视频关键词"""
    temp_path = None
    try:
        suffix = os.path.splitext(video.filename or "")[1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await video.read()
            tmp.write(content)
            temp_path = tmp.name

        result = await analyzer.extract_keywords(temp_path)

        if result.get("success"):
            return {"code": 200, "data": result}
        else:
            return {"code": 400, "message": result.get("error", "分析失败")}

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post("/emotion")
async def analyze_emotion(video: UploadFile = File(...)):
    """分析视频情绪"""
    temp_path = None
    try:
        suffix = os.path.splitext(video.filename or "")[1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await video.read()
            tmp.write(content)
            temp_path = tmp.name

        result = await analyzer.analyze_emotion(temp_path)

        if result.get("success"):
            return {"code": 200, "data": result}
        else:
            return {"code": 400, "message": result.get("error", "分析失败")}

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
