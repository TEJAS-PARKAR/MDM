from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from pathlib import Path
from app.core.config import settings
from app.pipeline.image_generator import image_generator
from app.pipeline.narrative_segmenter import narrative_segmenter, KamishibaiStory

router = APIRouter(prefix="/image", tags=["Visual Generation"])

class SinglePanelGenerateRequest(BaseModel):
    story_id: str
    panel_id: int
    prompt: str
    indian_style: str = "madhubani"
    japanese_style: str = "ukiyoe"
    camera_angle: str = "Wide shot"
    scene_title: str = ""
    force_regenerate: bool = False

class BatchGenerateRequest(BaseModel):
    story_id: str
    story_data: Optional[Dict] = None
    force_regenerate: bool = False

@router.post("/generate-panel")
async def generate_single_panel(req: SinglePanelGenerateRequest):
    """Generates an image for a specific Kamishibai panel."""
    try:
        path = image_generator.generate_panel_image(
            story_id=req.story_id,
            panel_id=req.panel_id,
            prompt=req.prompt,
            indian_style=req.indian_style,
            japanese_style=req.japanese_style,
            camera_angle=req.camera_angle,
            scene_title=req.scene_title,
            force_regenerate=req.force_regenerate
        )
        return {
            "status": "success",
            "story_id": req.story_id,
            "panel_id": req.panel_id,
            "image_url": f"/panels/{path.name}",
            "filename": path.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@router.post("/batch-generate")
async def batch_generate_panels(req: BatchGenerateRequest):
    """Generates all panel artwork for an entire Kamishibai story."""
    # Look up from active / preset stories or from request payload
    story = None
    if req.story_data:
        try:
            story = KamishibaiStory(**req.story_data)
        except Exception:
            pass

    if not story:
        story = narrative_segmenter.get_preset_story(req.story_id)

    if not story:
        raise HTTPException(status_code=404, detail=f"Story '{req.story_id}' not found.")

    generated_panels = []
    for panel in story.panels:
        try:
            path = image_generator.generate_panel_image(
                story_id=story.story_id,
                panel_id=panel.panel_id,
                prompt=panel.image_prompt,
                indian_style=story.indian_style,
                japanese_style=story.japanese_style,
                camera_angle=panel.camera_angle,
                scene_title=f"Card {panel.panel_id}",
                force_regenerate=req.force_regenerate
            )
            generated_panels.append({
                "panel_id": panel.panel_id,
                "image_url": f"/panels/{path.name}"
            })
        except Exception as e:
            print(f"[routes_image] Error generating panel {panel.panel_id}: {e}")

    return {
        "status": "success",
        "story_id": story.story_id,
        "total_generated": len(generated_panels),
        "panels": generated_panels
    }

@router.get("/panel/{story_id}/{panel_id}")
async def get_panel_image(story_id: str, panel_id: int):
    """Serves the generated panel image directly as a JPEG."""
    filename = f"{story_id}_panel_{panel_id}.jpg"
    filepath = settings.PANELS_DIR / filename
    if not filepath.exists():
        # Attempt on-demand generation from preset or active story
        story = narrative_segmenter.get_preset_story(story_id)
        if story and 0 < panel_id <= len(story.panels):
            panel = story.panels[panel_id - 1]
            filepath = image_generator.generate_panel_image(
                story_id=story_id,
                panel_id=panel_id,
                prompt=panel.image_prompt,
                indian_style=story.indian_style,
                japanese_style=story.japanese_style,
                camera_angle=panel.camera_angle
            )
        else:
            raise HTTPException(status_code=404, detail="Panel image not found.")

    return FileResponse(filepath, media_type="image/jpeg")
