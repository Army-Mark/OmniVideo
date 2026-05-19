import re
import httpx
from typing import Optional

from parsers.base_parser import BaseParser
from models.schemas import VideoInfo, Platform


class BilibiliParser(BaseParser):
    """B站视频解析器"""

    def __init__(self):
        super().__init__()
        self.platform = Platform.BILIBILI
        self.headers.update({
            "Referer": "https://www.bilibili.com/",
        })

    def can_handle(self, url: str) -> bool:
        patterns = [r"bilibili\.com", r"b23\.tv"]
        return any(re.search(p, url) for p in patterns)

    async def parse(self, url: str) -> Optional[VideoInfo]:
        try:
            bvid = self._extract_bvid(url)
            if not bvid:
                return None

            info_url = "https://api.bilibili.com/x/web-interface/view"
            params = {"bvid": bvid}

            async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
                response = await client.get(info_url, params=params, timeout=30)
                data = response.json()

            if data.get("code") != 0:
                return None

            video_data = data.get("data", {})
            owner = video_data.get("owner", {})
            stat = video_data.get("stat", {})

            cid = video_data.get("cid")
            video_url = await self._get_video_url(bvid, cid) if cid else None

            return VideoInfo(
                video_id=bvid,
                platform=Platform.BILIBILI,
                title=video_data.get("title", ""),
                description=video_data.get("desc", ""),
                cover_url=video_data.get("pic", ""),
                video_url=video_url,
                duration=video_data.get("duration", 0),
                width=0,
                height=0,
                author=owner.get("name", ""),
                author_avatar=owner.get("face", ""),
                like_count=stat.get("like", 0),
                share_count=stat.get("share", 0),
                comment_count=stat.get("reply", 0),
            )

        except Exception as e:
            print(f"B站解析错误: {e}")
            return None

    def _extract_bvid(self, url: str) -> Optional[str]:
        patterns = [
            r"/video/(BV\w+)",
            r"bvid=(BV\w+)",
            r"b23\.tv/\w+",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                if "b23.tv" in url:
                    return None
                return match.group(1)
        if url.startswith("BV"):
            return url
        return None

    async def _get_video_url(self, bvid: str, cid: int) -> Optional[str]:
        try:
            play_url = "https://api.bilibili.com/x/player/playurl"
            params = {
                "bvid": bvid,
                "cid": cid,
                "fnval": "16",
            }
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.get(play_url, params=params, timeout=30)
                data = response.json()

            if data.get("code") == 0:
                dash = data.get("data", {}).get("dash")
                if dash:
                    videos = dash.get("video", [])
                    if videos:
                        return videos[0].get("baseUrl")
                durl = data.get("data", {}).get("durl", [])
                if durl:
                    return durl[0].get("url")
            return None
        except Exception:
            return None
