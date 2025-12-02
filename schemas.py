from pydantic import BaseModel, Field
from typing import Literal, Union


class VideoPrompt(BaseModel):
    """Schema for video prompt JSON output"""
    id: str = Field(..., description="Short identifier for the video")
    type: Literal["video"] = "video"
    model: Literal["video-model"] = "video-model"
    topic: str = Field(..., description="Short description of the finance topic or meme")
    hook: str = Field(..., description="Strong 1-sentence hook aimed at TikTok viewers")
    prompt: str = Field(..., description="Full production prompt for the model")
    duration_seconds: int = Field(..., ge=5, le=30, description="Video duration between 5-30 seconds")
    aspect_ratio: Literal["9:16"] = "9:16"
    style_notes: str = Field(..., description="Very short extra style hints")
    cta_overlay: str = Field(default="", description="Optional on-screen text idea")
    language: Literal["en"] = "en"


class ImagePrompt(BaseModel):
    """Schema for image prompt JSON output"""
    id: str = Field(..., description="Short identifier for the image")
    type: Literal["image"] = "image"
    model: Literal["gpt-image-1-mini"] = "gpt-image-1-mini"
    topic: str = Field(..., description="Short description of the finance topic or meme")
    hook: str = Field(..., description="Strong 1-sentence hook aimed at TikTok viewers")
    prompt: str = Field(..., description="Full production prompt for the model")
    duration_seconds: Literal[0] = 0
    aspect_ratio: Literal["9:16"] = "9:16"
    style_notes: str = Field(..., description="Very short extra style hints")
    cta_overlay: str = Field(default="", description="Optional on-screen text idea")
    language: Literal["en"] = "en"


class ContentOutput(BaseModel):
    """Container for all generated content"""
    prompts: list[Union[VideoPrompt, ImagePrompt]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompts": [
                    {
                        "id": "example-video",
                        "type": "video",
                        "model": "video-model",
                        "topic": "Bitcoin halving event",
                        "hook": "This event only happens every 4 years.",
                        "prompt": "A cinematic shot...",
                        "duration_seconds": 10,
                        "aspect_ratio": "9:16",
                        "style_notes": "thriller, dramatic",
                        "cta_overlay": "Are you ready?",
                        "language": "en"
                    }
                ]
            }
        }
