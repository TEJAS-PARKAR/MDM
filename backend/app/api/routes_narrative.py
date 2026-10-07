from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.core.config import settings
from app.pipeline.narrative_segmenter import (
    narrative_segmenter,
    KamishibaiStory,
    PRESET_STORIES
)

router = APIRouter(prefix="/narrative", tags=["Narrative Orchestration"])

class StoryInputRequest(BaseModel):
    title: str = "The Panchatantra Tale"
    source: str = "Panchatantra"
    story_text: str
    indian_style: str = "madhubani"
    japanese_style: str = "ukiyoe"

class PromptFormatRequest(BaseModel):
    scene_action: str
    character_details: str
    indian_style: str = "madhubani"
    japanese_style: str = "ukiyoe"
    camera_angle: str = "Wide establishing shot"

@router.get("/presets")
async def get_preset_stories():
    """Returns metadata for all pre-configured Panchatantra & Jataka tales."""
    return narrative_segmenter.get_presets()

@router.get("/presets/{story_id}", response_model=KamishibaiStory)
async def get_preset_story_detail(story_id: str):
    """Retrieves full Kamishibai story data for a preset by story ID."""
    story = narrative_segmenter.get_preset_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail=f"Story with ID '{story_id}' not found.")
    return story

@router.get("/styles")
async def get_available_styles():
    """Returns all available Indian Folk, Japanese Traditional, and Fusion Art styles."""
    return {
        "indian_styles": settings.INDIAN_STYLES,
        "japanese_styles": settings.JAPANESE_STYLES,
        "recommended_fusions": [
            {
                "id": "madhubani_ukiyoe",
                "indian": "madhubani",
                "japanese": "ukiyoe",
                "name": "Mithila Geometry × Edo Woodblock",
                "vibe": "Sacred nature geometry with Hokusai ocean foam and subtle bokashi gradients"
            },
            {
                "id": "warli_sumie",
                "indian": "warli",
                "japanese": "sumie",
                "name": "Warli Tribal × Zen Ink Wash",
                "vibe": "Terracotta mud and white rice geometric stick figures amidst Zen misty mountains and splashed ink"
            },
            {
                "id": "pattachitra_anime",
                "indian": "pattachitra",
                "japanese": "anime90s",
                "name": "Pattachitra Scroll × 90s Cel Anime",
                "vibe": "Lyrical cloth scroll borders with expressive hand-painted cel animation and nostalgic warm grain"
            }
        ]
    }

@router.post("/segment", response_model=KamishibaiStory)
async def segment_story_endpoint(req: StoryInputRequest):
    """
    Decomposes raw story text into sequential theatrical Kamishibai panels
    with trilingual dialogue, stage directions, and style-infused prompts.
    """
    if not req.story_text.strip():
        raise HTTPException(status_code=400, detail="Story text cannot be empty.")

    story = narrative_segmenter.segment_story(
        story_text=req.story_text,
        title=req.title,
        source=req.source,
        indian_style=req.indian_style,
        japanese_style=req.japanese_style
    )
    return story

@router.post("/format-prompt")
async def format_prompt_endpoint(req: PromptFormatRequest):
    """Formats an optimized Stable Diffusion XL / FLUX prompt for a single panel."""
    from app.core.prompts import FUSION_PROMPT_TEMPLATE
    
    ind = settings.INDIAN_STYLES.get(req.indian_style, settings.INDIAN_STYLES["madhubani"])
    jap = settings.JAPANESE_STYLES.get(req.japanese_style, settings.JAPANESE_STYLES["ukiyoe"])

    prompt = FUSION_PROMPT_TEMPLATE.format(
        scene_action=req.scene_action,
        character_details=req.character_details,
        indian_style_keywords=ind["keywords"],
        japanese_style_keywords=jap["keywords"],
        camera_angle=req.camera_angle
    )
    return {"prompt": prompt}
