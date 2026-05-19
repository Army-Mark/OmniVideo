from abc import ABC, abstractmethod
from typing import Optional
from models.schemas import VideoInfo, Platform


class BaseParser(ABC):
    """解析器基类"""

    def __init__(self):
        self.platform: Platform = Platform.OTHER
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

    @abstractmethod
    async def parse(self, url: str) -> Optional[VideoInfo]:
        """解析视频链接，返回视频信息"""
        pass

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """判断是否能处理该链接"""
        pass

    def _extract_video_id(self, url: str) -> Optional[str]:
        """从链接中提取视频ID"""
        return None
