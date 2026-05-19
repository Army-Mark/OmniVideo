from typing import Optional, List
from parsers.base_parser import BaseParser
from parsers.douyin_parser import DouyinParser
from parsers.bilibili_parser import BilibiliParser
from parsers.xiaohongshu_parser import XiaohongshuParser
from models.schemas import VideoInfo


class ParserFactory:
    """解析器工厂

    采用工厂模式，根据URL自动选择对应的解析器
    参考: wwwzhouhui/video-parser 的 downloader_factory.py
    """

    _parsers: List[BaseParser] = []

    @classmethod
    def _init_parsers(cls):
        if not cls._parsers:
            cls._parsers = [
                DouyinParser(),
                BilibiliParser(),
                XiaohongshuParser(),
            ]

    @classmethod
    def get_parser(cls, url: str) -> Optional[BaseParser]:
        cls._init_parsers()
        for parser in cls._parsers:
            if parser.can_handle(url):
                return parser
        return None

    @classmethod
    async def parse(cls, url: str) -> Optional[VideoInfo]:
        parser = cls.get_parser(url)
        if parser:
            return await parser.parse(url)
        return None

    @classmethod
    def register_parser(cls, parser: BaseParser):
        cls._init_parsers()
        cls._parsers.append(parser)
