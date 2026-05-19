import uuid
import httpx
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import DownloadRequest, DownloadResponse, DownloadTask, DownloadStatus
from models.database import settings

router = APIRouter()

download_tasks = {}


@router.post("/", response_model=DownloadResponse)
async def create_download_task(
    request: DownloadRequest,
    background_tasks: BackgroundTasks,
):
    """创建下载任务"""
    task_id = str(uuid.uuid4())

    task = DownloadTask(
        task_id=task_id,
        video_info=None,
        status=DownloadStatus.PENDING,
    )

    download_tasks[task_id] = task

    background_tasks.add_task(process_download, task_id, request)

    return DownloadResponse(
        code=200,
        message="下载任务已创建",
        data=task,
    )


@router.get("/{task_id}")
async def get_download_status(task_id: str):
    """获取下载任务状态"""
    task = download_tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {
        "code": 200,
        "data": task,
    }


@router.post("/{task_id}/pause")
async def pause_download(task_id: str):
    """暂停下载"""
    task = download_tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.DOWNLOAD_ENGINE_URL}/download/{task_id}/pause")
    except Exception:
        pass

    task.status = DownloadStatus.PAUSED
    return {"code": 200, "message": "已暂停"}


@router.post("/{task_id}/resume")
async def resume_download(task_id: str):
    """继续下载"""
    task = download_tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.DOWNLOAD_ENGINE_URL}/download/{task_id}/resume")
    except Exception:
        pass

    task.status = DownloadStatus.DOWNLOADING
    return {"code": 200, "message": "已继续"}


@router.delete("/{task_id}")
async def cancel_download(task_id: str):
    """取消下载"""
    task = download_tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    try:
        async with httpx.AsyncClient() as client:
            await client.delete(f"{settings.DOWNLOAD_ENGINE_URL}/download/{task_id}")
    except Exception:
        pass

    task.status = DownloadStatus.FAILED
    task.error_message = "用户取消"
    return {"code": 200, "message": "已取消"}


@router.get("/")
async def list_downloads():
    """获取下载列表"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{settings.DOWNLOAD_ENGINE_URL}/downloads")
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass

    return {
        "code": 200,
        "data": list(download_tasks.values()),
    }


async def process_download(task_id: str, request: DownloadRequest):
    """将下载任务转发到 Go 下载引擎"""
    task = download_tasks.get(task_id)
    if not task:
        return

    task.status = DownloadStatus.DOWNLOADING

    try:
        async with httpx.AsyncClient(timeout=300) as client:
            resp = await client.post(
                f"{settings.DOWNLOAD_ENGINE_URL}/download",
                json={"url": request.video_url},
            )
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                task.file_path = data.get("file_path")
                task.file_size = data.get("file_size", 0)
            else:
                task.status = DownloadStatus.FAILED
                task.error_message = f"下载引擎返回错误: HTTP {resp.status_code}"
    except httpx.ConnectError:
        task.status = DownloadStatus.FAILED
        task.error_message = "无法连接下载引擎"
    except Exception as e:
        task.status = DownloadStatus.FAILED
        task.error_message = str(e)
