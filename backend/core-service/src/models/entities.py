from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from models.database import Base


class PlatformEnum(str, enum.Enum):
    DOUYIN = "douyin"
    BILIBILI = "bilibili"
    XIAOHONGSHU = "xiaohongshu"
    KUAISHOU = "kuaishou"
    YOUTUBE = "youtube"
    PIPIXIA = "pipixia"
    HAOKAN = "haokan"
    OTHER = "other"


class DownloadStatusEnum(str, enum.Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar = Column(String(500), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    download_history = relationship("DownloadHistory", back_populates="user")
    parse_history = relationship("ParseHistory", back_populates="user")


class DownloadHistory(Base):
    __tablename__ = "download_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    task_id = Column(String(36), unique=True, nullable=False, index=True)
    video_id = Column(String(100), nullable=False)
    platform = Column(SQLEnum(PlatformEnum), nullable=False)
    title = Column(String(500), default="")
    video_url = Column(String(2000), default="")
    file_path = Column(String(1000), default="")
    file_size = Column(Integer, default=0)
    status = Column(SQLEnum(DownloadStatusEnum), default=DownloadStatusEnum.PENDING)
    progress = Column(Float, default=0.0)
    error_message = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="download_history")


class ParseHistory(Base):
    __tablename__ = "parse_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    url = Column(String(2000), nullable=False)
    video_id = Column(String(100), nullable=False)
    platform = Column(SQLEnum(PlatformEnum), nullable=False)
    title = Column(String(500), default="")
    author = Column(String(100), default="")
    cover_url = Column(String(2000), default="")
    video_url = Column(String(2000), default="")
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="parse_history")
