import re
import httpx
from typing import Optional

from parsers.base_parser import BaseParser
from models.schemas import VideoInfo, Platform


class XiaohongshuParser(BaseParser):
    """小红书视频解析器

    参考项目: liu-ziting/xhs-parser
    """

    def __init__(self):
        super().__init__()
        self.platform = Platform.XIAOHONGSHU
        self.headers.update({
            "Referer": "https://www.xiaohongshu.com/",
        })

    def can_handle(self, url: str) -> bool:
        patterns = [
            r"xiaohongshu\.com",
            r"xhslink\.com",
        ]
        return any(re.search(p, url) for p in patterns)

    async def parse(self, url: str) -> Optional[VideoInfo]:
        try:
            note_id = self._extract_note_id(url)
            if not note_id:
                return None

            share_url = f"https://www.xiaohongshu.com/explore/{note_id}"

            async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
                response = await client.get(share_url, timeout=30)
                html = response.text

            import json
            match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?})\s*</script>', html, re.DOTALL)
            if not match:
                return None

            state = json.loads(match.group(1))
            note_data = state.get("note", {}).get("noteDetailMap", {}).get(note_id, {}).get("note", {})

            if not note_data:
                return None

            title = note_data.get("title", "") or note_data.get("desc", "")[:50]
            desc = note_data.get("desc", "")

            video_url = None
            cover_url = None

            image_list = note_data.get("imageList", [])
            if image_list:
                cover_url = image_list[0].get("urlDefault", "")

            video_info = note_data.get("video", {})
            if video_info:
                media = video_info.get("media", {})
                video_data = media.get("video", {})
                if video_url := video_data.get("masterUrl"):
                    pass
                elif h264 := video_data.get("h264", []):
                    if h264:
                        video_url = h264[0].get("masterUrl")

            user_info = note_data.get("user", {})
            interact_info = note_data.get("interactInfo", {})

            return VideoInfo(
                video_id=note_id,
                platform=Platform.XIAOHONGSHU,
                title=title,
                description=desc,
                cover_url=cover_url,
                video_url=video_url,
                author=user_info.get("nickname", ""),
                author_avatar=user_info.get("avatar", ""),
                like_count=int(interact_info.get("likedCount", 0)),
                share_count=int(interact_info.get("shareCount", 0)),
                comment_count=int(interact_info.get("commentCount", 0)),
            )

        except Exception as e:
            print(f"小红书解析错误: {e}")
            return None

    def _extract_note_id(self, url: str) -> Optional[str]:
        patterns = [
            r"/explore/([a-f0-9]+)",
            r"/discovery/item/([a-f0-9]+)",
            r"xhslink\.com/\w+\?.*shareId=([a-f0-9]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
