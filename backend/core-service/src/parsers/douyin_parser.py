import re
import json
import httpx
from typing import Optional
from urllib.parse import urlparse, parse_qs

from parsers.base_parser import BaseParser
from models.schemas import VideoInfo, Platform


class DouyinParser(BaseParser):
    """抖音视频解析器

    参考项目: Evil0ctal/Douyin_TikTok_Download_API
    使用 X-Bogus 算法请求抖音 Web API
    """

    def __init__(self):
        super().__init__()
        self.platform = Platform.DOUYIN
        self.headers.update({
            "Referer": "https://www.douyin.com/",
            "Cookie": "",
        })

    def can_handle(self, url: str) -> bool:
        patterns = [
            r"douyin\.com",
            r"iesdouyin\.com",
            r"v\.douyin\.com",
        ]
        return any(re.search(p, url) for p in patterns)

    async def parse(self, url: str) -> Optional[VideoInfo]:
        try:
            video_id = self._extract_video_id(url)
            if not video_id:
                return None

            detail_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/"
            params = {
                "aweme_id": video_id,
                "aid": "1128",
                "version_name": "23.5.0",
            }

            async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
                response = await client.get(detail_url, params=params, timeout=30)
                data = response.json()

            if data.get("status_code") != 0:
                return None

            aweme_detail = data.get("aweme_detail", {})
            if not aweme_detail:
                return None

            video_info = aweme_detail.get("video", {})
            author_info = aweme_detail.get("author", {})
            statistics = aweme_detail.get("statistics", {})

            video_url = self._extract_video_url(video_info)
            cover_url = self._extract_cover_url(video_info)

            return VideoInfo(
                video_id=video_id,
                platform=Platform.DOUYIN,
                title=aweme_detail.get("desc", ""),
                description=aweme_detail.get("desc", ""),
                cover_url=cover_url,
                video_url=video_url,
                duration=video_info.get("duration", 0),
                width=video_info.get("width", 0),
                height=video_info.get("height", 0),
                author=author_info.get("nickname", ""),
                author_avatar=author_info.get("avatar_thumb", {}).get("url_list", [None])[0],
                like_count=statistics.get("digg_count", 0),
                share_count=statistics.get("share_count", 0),
                comment_count=statistics.get("comment_count", 0),
                is_live=aweme_detail.get("is_live", False),
            )

        except Exception as e:
            print(f"抖音解析错误: {e}")
            return None

    def _extract_video_id(self, url: str) -> Optional[str]:
        patterns = [
            r"/video/(\d+)",
            r"modal_id=(\d+)",
            r"/note/(\d+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        parsed = urlparse(url)
        if "v.douyin.com" in parsed.netloc:
            return None

        return None

    def _extract_video_url(self, video_info: dict) -> Optional[str]:
        play_addr = video_info.get("play_addr", {})
        url_list = play_addr.get("url_list", [])
        if url_list:
            return url_list[0].replace("playwm", "play")
        return None

    def _extract_cover_url(self, video_info: dict) -> Optional[str]:
        cover = video_info.get("cover", {})
        url_list = cover.get("url_list", [])
        if url_list:
            return url_list[0]
        return None
