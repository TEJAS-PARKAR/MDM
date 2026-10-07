from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from pathlib import Path
from app.core.config import settings
from app.pipeline.tts_generator import tts_generator
from app.pipeline.narrative_segmenter import narrative_segmenter
from app.pipeline.wav2lip_runner import wav2lip_runner

router = APIRouter(prefix="/audio", tags=["Multilingual Audio Narration"])

class SingleAudioSynthesizeRequest(BaseModel):
    story_id: str
    panel_id: int
    text: str
    lang: str = "en"  # "en", "hi", "ja"
    voice_rate: str = "+0%"
    voice_pitch: str = "+0Hz"
    force_regenerate: bool = False

class BatchAudioSynthesizeRequest(BaseModel):
    story_id: str
    story_data: Optional[Dict] = None
    force_regenerate: bool = False

class Wav2LipRequest(BaseModel):
    story_id: str
    panel_id: int
    lang: str = "en"

@router.post("/synthesize")
async def synthesize_single_panel_audio(req: SingleAudioSynthesizeRequest):
    """Synthesizes speech audio for a specific panel in EN, HI, or JA."""
    if req.lang not in ["en", "hi", "ja"]:
        raise HTTPException(status_code=400, detail="Supported languages are 'en', 'hi', and 'ja'.")

    try:
        path = await tts_generator.synthesize_speech_async(
            text=req.text,
            lang=req.lang,
            story_id=req.story_id,
            panel_id=req.panel_id,
            voice_rate=req.voice_rate,
            voice_pitch=req.voice_pitch,
            force_regenerate=req.force_regenerate
        )
        return {
            "status": "success",
            "story_id": req.story_id,
            "panel_id": req.panel_id,
            "lang": req.lang,
            "audio_url": f"/audio/{path.name}",
            "filename": path.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio synthesis error: {str(e)}")

@router.post("/batch-synthesize")
async def batch_synthesize_audio(req: BatchAudioSynthesizeRequest):
    """Synthesizes all audio tracks across all 3 languages for a story."""
    story = None
    if req.story_data:
        try:
            from app.pipeline.narrative_segmenter import KamishibaiStory
            story = KamishibaiStory(**req.story_data)
        except Exception:
            pass

    if not story:
        story = narrative_segmenter.get_preset_story(req.story_id)

    if not story:
        raise HTTPException(status_code=404, detail=f"Story '{req.story_id}' not found.")

    results = await tts_generator.batch_synthesize_story(story, force_regenerate=req.force_regenerate)
    return {
        "status": "success",
        "story_id": req.story_id,
        "tracks": results
    }

@router.get("/stream/{story_id}/{panel_id}/{lang}")
async def stream_panel_audio(story_id: str, panel_id: int, lang: str):
    """Streams narration audio for a specific panel and language."""
    filename = f"{story_id}_panel_{panel_id}_{lang}.mp3"
    filepath = settings.AUDIO_DIR / filename
    
    if not filepath.exists():
        # Check if .wav exists
        wav_path = settings.AUDIO_DIR / f"{story_id}_panel_{panel_id}_{lang}.wav"
        if wav_path.exists():
            return FileResponse(wav_path, media_type="audio/wav")
            
        # On-demand synthesis from preset
        story = narrative_segmenter.get_preset_story(story_id)
        if story and 0 < panel_id <= len(story.panels):
            panel = story.panels[panel_id - 1]
            text = getattr(panel.dialogue, lang, panel.dialogue.en)
            filepath = await tts_generator.synthesize_speech_async(
                text=text,
                lang=lang,
                story_id=story_id,
                panel_id=panel_id
            )
        else:
            raise HTTPException(status_code=404, detail="Audio file not found.")

    media_type = "audio/mpeg" if filepath.suffix == ".mp3" else "audio/wav"
    return FileResponse(filepath, media_type=media_type)

@router.get("/sound-effect/{sfx_name}")
async def get_sound_effect(sfx_name: str):
    """Returns traditional Kamishibai sound effects (hyoshigi, taiko, paper_slide)."""
    valid_sfx = ["hyoshigi", "taiko", "paper_slide"]
    if sfx_name not in valid_sfx:
        raise HTTPException(status_code=404, detail=f"SFX '{sfx_name}' not found. Valid: {valid_sfx}")

    filepath = settings.AUDIO_DIR / f"{sfx_name}.wav"
    if not filepath.exists():
        tts_generator._ensure_sound_effects()

    return FileResponse(filepath, media_type="audio/wav")

@router.post("/wav2lip")
async def generate_wav2lip_preview(req: Wav2LipRequest):
    """Generates a talking character lip-synced video clip for a panel."""
    image_file = settings.PANELS_DIR / f"{req.story_id}_panel_{req.panel_id}.jpg"
    audio_file = settings.AUDIO_DIR / f"{req.story_id}_panel_{req.panel_id}_{req.lang}.mp3"
    
    if not image_file.exists():
        # Ensure image is generated
        story = narrative_segmenter.get_preset_story(req.story_id)
        if story and 0 < req.panel_id <= len(story.panels):
            p = story.panels[req.panel_id - 1]
            from app.pipeline.image_generator import image_generator
            image_file = image_generator.generate_panel_image(
                story_id=req.story_id,
                panel_id=req.panel_id,
                prompt=p.image_prompt,
                indian_style=story.indian_style,
                japanese_style=story.japanese_style
            )

    if not audio_file.exists():
        story = narrative_segmenter.get_preset_story(req.story_id)
        if story and 0 < req.panel_id <= len(story.panels):
            p = story.panels[req.panel_id - 1]
            text = getattr(p.dialogue, req.lang, p.dialogue.en)
            audio_file = await tts_generator.synthesize_speech_async(
                text=text,
                lang=req.lang,
                story_id=req.story_id,
                panel_id=req.panel_id
            )

    output_video = settings.STATIC_DIR / "videos" / f"{req.story_id}_panel_{req.panel_id}_{req.lang}.mp4"
    result = wav2lip_runner.generate_lip_sync_video(
        image_path=image_file,
        audio_path=audio_file,
        output_path=output_video
    )
    return result
