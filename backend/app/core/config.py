import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Dict, List

# Base directory for the backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Kamishibai: Indo-Japanese Visual Storytelling Platform"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Storage Paths
    STATIC_DIR: Path = BASE_DIR / "static"
    PANELS_DIR: Path = BASE_DIR / "static" / "panels"
    AUDIO_DIR: Path = BASE_DIR / "static" / "audio"
    PRESETS_DIR: Path = BASE_DIR / "static" / "presets"
    
    # Frontend public path sync (for instant static Next.js serving)
    FRONTEND_PUBLIC_DIR: Path = BASE_DIR.parent / "frontend" / "public"
    FRONTEND_PANELS_DIR: Path = BASE_DIR.parent / "frontend" / "public" / "panels"
    FRONTEND_AUDIO_DIR: Path = BASE_DIR.parent / "frontend" / "public" / "audio"

    # API Keys (optional; system falls back to high-grade local neural & procedural generators)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    STABILITY_API_KEY: str = os.getenv("STABILITY_API_KEY", "")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")

    # Visual Generation Settings
    SDXL_MODEL_ID: str = os.getenv("SDXL_MODEL_ID", "stabilityai/stable-diffusion-xl-base-1.0")
    DEVICE: str = os.getenv("DEVICE", "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu")
    IMAGE_WIDTH: int = 1024
    IMAGE_HEIGHT: int = 768  # 4:3 traditional Kamishibai card ratio

    # Neural Voices for Multilingual TTS
    VOICE_CONFIG: Dict[str, Dict[str, str]] = {
        "en": {
            "primary": "en-US-ChristopherNeural",
            "expressive": "en-IN-PrabhatNeural",
            "female": "en-IN-NeerjaNeural",
            "label": "English (Storyteller)"
        },
        "hi": {
            "primary": "hi-IN-MadhurNeural",
            "expressive": "hi-IN-SwaraNeural",
            "female": "hi-IN-SwaraNeural",
            "label": "हिन्दी (कथावाचक)"
        },
        "ja": {
            "primary": "ja-JP-NanamiNeural",
            "expressive": "ja-JP-KeitaNeural",
            "female": "ja-JP-NanamiNeural",
            "label": "日本語 (紙芝居師)"
        }
    }

    # Style Presets
    INDIAN_STYLES: Dict[str, Dict[str, str]] = {
        "madhubani": {
            "name": "Madhubani (Mithila Art)",
            "origin": "Bihar, India",
            "description": "Intricate geometric motifs, double outlines, natural mineral colors, and nature symbolism (peacocks, lotus, fish).",
            "keywords": "Madhubani folk art, Mithila painting style, intricate fine double black outlines, vibrant natural plant dye colors, geometric floral borders, stylized folk figures, mineral pigments on handmade paper texture"
        },
        "warli": {
            "name": "Warli Tribal Art",
            "origin": "Maharashtra, India",
            "description": "Primitive geometric elegance, circles and triangles symbolizing sun, moon, and balance of nature on terracotta mud walls.",
            "keywords": "Warli tribal art style, rustic terracotta red clay background, white rice-paste paint, geometric stick figures, tarpa dance circle, stylized trees and deer, sacred geometric harmony, authentic tribal wall painting"
        },
        "pattachitra": {
            "name": "Pattachitra Scroll Art",
            "origin": "Odisha / Bengal, India",
            "description": "Mythological cloth scroll painting with bold black contour lines, rich crimson and indigo, and ornate border framing.",
            "keywords": "Odisha Pattachitra scroll painting, traditional cloth canvas texture, bold lyrical black contour linework, rich crimson indigo and gold tempera hues, elaborate decorative floral borders, mythological miniature detail"
        }
    }

    JAPANESE_STYLES: Dict[str, Dict[str, str]] = {
        "ukiyoe": {
            "name": "Ukiyo-e (Woodblock Prints)",
            "origin": "Edo Period, Japan",
            "description": "Floating world aesthetic by masters like Hokusai and Hiroshige, with flat color planes, bokashi gradations, and bold outlines.",
            "keywords": "Edo period Ukiyo-e woodblock print, Hokusai and Hiroshige aesthetic, delicate washi paper grain, subtle bokashi gradation shading, relief woodcut outlines, traditional Japanese pigment color palette"
        },
        "sumie": {
            "name": "Sumi-e (Suibokuga Ink Wash)",
            "origin": "Muromachi Period, Japan",
            "description": "Zen-inspired black ink wash painting emphasizing the beauty of simplicity, negative space (ma), and energetic brushwork.",
            "keywords": "Sumi-e suibokuga ink wash painting, dynamic Zen calligraphy brushstrokes, splashed haboku ink technique, harmonious negative space ma, monochrome charcoal to silver gradients on fibrous rice paper"
        },
        "anime90s": {
            "name": "90s Retro Cel Anime",
            "origin": "Showa/Heisei Era, Japan",
            "description": "Hand-painted cel animation look with visible grain, nostalgic warm lighting, expressive character eyes, and classic theatrical depth.",
            "keywords": "1990s retro anime aesthetic, hand-drawn cel shading, authentic 35mm film grain, Studio Ghibli and classic Toei visual warmth, rich dramatic atmospheric lighting, expressive emotive character design"
        }
    }

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
for directory in [
    settings.STATIC_DIR,
    settings.PANELS_DIR,
    settings.AUDIO_DIR,
    settings.PRESETS_DIR,
    settings.FRONTEND_PANELS_DIR,
    settings.FRONTEND_AUDIO_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)
