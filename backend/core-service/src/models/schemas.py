from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    DOUYIN = "douyin"
    BILIBILI = "bilibili"
    XIAOHONGSHU = "xiaohongshu"
    KUAISHOU = "kuaishou"
    YOUTUBE = "youtube"
    PIPIXIA = "pipixia"
    HAOKAN = "haokan"
    OTHER = "other"


class VideoInfo(BaseModel):
    video_id: str
    platform: Platform
    title: str
    description: Optional[str] = None
    cover_url: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    author: Optional[str] = None
    author_avatar: Optional[str] = None
    like_count: Optional[int] = None
    share_count: Optional[int] = None
    comment_count: Optional[int] = None
    is_live: bool = False
    created_at: Optional[datetime] = None


class ParseRequest(BaseModel):
    url: str = Field(..., description="视频链接")


class ParseResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[VideoInfo] = None


class DownloadStatus(str, Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class DownloadTask(BaseModel):
    task_id: str
    video_info: VideoInfo
    status: DownloadStatus = DownloadStatus.PENDING
    progress: float = 0.0
    speed: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class DownloadRequest(BaseModel):
    video_url: str
    video_id: str
    quality: Optional[str] = "hd"


class DownloadResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[DownloadTask] = None


class AIAnalysisRequest(BaseModel):
    video_path: str
    prompt: Optional[str] = "请描述这个视频的内容"
    max_frames: int = 6


class AIAnalysisResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str] = None
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class HistoryResponse(BaseModel):
    id: int
    video_info: VideoInfo
    action: str
    created_at: datetime
