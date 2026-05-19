import os
import base64
import subprocess
import tempfile
from typing import Optional, List
from pathlib import Path

from openai import AsyncOpenAI
from pydantic_settings import BaseSettings


class AISettings(BaseSettings):
    QWEN_API_KEY: str = ""
    QWEN_API_BASE_URL: str = "https://api-inference.modelscope.cn/v1"
    QWEN_MODEL_ID: str = "Qwen/Qwen3-VL-8B-Instruct"
    MAX_FRAMES: int = 6

    class Config:
        env_file = ".env"


class Qwen3VLAnalyzer:
    """AI 视频内容分析器

    参考项目: wwwzhouhui/video-parser 的 qwen3vl.py
    使用 Qwen3-VL 模型分析视频内容
    """

    def __init__(self, settings: Optional[AISettings] = None):
        self.settings = settings or AISettings()
        self.client = AsyncOpenAI(
            api_key=self.settings.QWEN_API_KEY,
            base_url=self.settings.QWEN_API_BASE_URL,
        )

    async def analyze_video(
        self,
        video_path: str,
        prompt: str = "请详细描述这个视频的内容，包括场景、人物、动作、情绪等",
        max_frames: Optional[int] = None,
    ) -> dict:
        """分析视频内容"""
        frames = await self._extract_frames(video_path, max_frames or self.settings.MAX_FRAMES)
        if not frames:
            return {"success": False, "error": "无法提取视频帧"}

        base64_frames = [self._image_to_base64(frame) for frame in frames]

        try:
            response = await self.client.chat.completions.create(
                model=self.settings.QWEN_MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            *[
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{frame}"},
                                }
                                for frame in base64_frames
                            ],
                        ],
                    }
                ],
                max_tokens=1024,
            )

            return {
                "success": True,
                "analysis": response.choices[0].message.content,
                "frames_analyzed": len(base64_frames),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _extract_frames(self, video_path: str, max_frames: int) -> List[str]:
        """从视频中提取关键帧"""
        frames = []
        temp_dir = tempfile.mkdtemp()

        try:
            probe_cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                video_path,
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            import json
            duration = float(json.loads(result.stdout)["format"]["duration"])

            interval = duration / (max_frames + 1)

            for i in range(max_frames):
                timestamp = interval * (i + 1)
                output_path = os.path.join(temp_dir, f"frame_{i}.jpg")

                cmd = [
                    "ffmpeg",
                    "-ss", str(timestamp),
                    "-i", video_path,
                    "-vframes", "1",
                    "-q:v", "2",
                    "-y",
                    output_path,
                ]
                subprocess.run(cmd, capture_output=True)

                if os.path.exists(output_path):
                    frames.append(output_path)

        except Exception as e:
            print(f"提取视频帧错误: {e}")

        return frames

    def _image_to_base64(self, image_path: str) -> str:
        """将图片转换为 base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    async def generate_summary(self, video_path: str) -> dict:
        """生成视频摘要"""
        prompt = "请用简洁的语言总结这个视频的主要内容，不超过100字"
        return await self.analyze_video(video_path, prompt)

    async def extract_keywords(self, video_path: str) -> dict:
        """提取视频关键词"""
        prompt = "请从视频中提取5-10个关键词，用逗号分隔"
        result = await self.analyze_video(video_path, prompt)
        if result.get("success"):
            keywords = result["analysis"].split("，")
            result["keywords"] = [k.strip() for k in keywords if k.strip()]
        return result

    async def analyze_emotion(self, video_path: str) -> dict:
        """分析视频情绪"""
        prompt = "请分析视频的整体情绪氛围（如：欢快、温馨、紧张、悲伤等），并给出理由"
        return await self.analyze_video(video_path, prompt)
