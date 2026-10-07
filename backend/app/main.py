import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.routes_narrative import router as narrative_router
from app.api.routes_image import router as image_router
from app.api.routes_audio import router as audio_router
from app.pipeline.narrative_segmenter import narrative_segmenter
from app.pipeline.image_generator import image_generator
from app.pipeline.tts_generator import tts_generator

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Cross-Cultural Generative AI Engine adapting Indian folk tales into Japanese Kamishibai street-theater format."
)

# CORS setup for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Directories for direct browser asset loading
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
app.mount("/panels", StaticFiles(directory=str(settings.PANELS_DIR)), name="panels")
app.mount("/audio", StaticFiles(directory=str(settings.AUDIO_DIR)), name="audio")

# Include Routers
app.include_router(narrative_router, prefix=settings.API_PREFIX)
app.include_router(image_router, prefix=settings.API_PREFIX)
app.include_router(audio_router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    """
    On startup, pre-generates demo assets for the flagship Panchatantra story
    ('The Monkey and the Crocodile') so the frontend can load immediately with zero latency.
    """
    print("[AI-Kamishibai] Initializing platform and ensuring demo assets...")
    try:
        # Pre-seed sound effects
        tts_generator._ensure_sound_effects()

        # Seed flagship Panchatantra story
        story = narrative_segmenter.get_preset_story("monkey-and-crocodile")
        if story:
            print(f"[AI-Kamishibai] Pre-generating panels and audio for: {story.title}...")
            # 1. Generate panels
            for panel in story.panels:
                image_generator.generate_panel_image(
                    story_id=story.story_id,
                    panel_id=panel.panel_id,
                    prompt=panel.image_prompt,
                    indian_style=story.indian_style,
                    japanese_style=story.japanese_style,
                    camera_angle=panel.camera_angle
                )
            
            # 2. Synthesize audio asynchronously in background
            asyncio.create_task(tts_generator.batch_synthesize_story(story))
            print("[AI-Kamishibai] Flagship story initialized successfully.")
    except Exception as e:
        print(f"[AI-Kamishibai] Startup asset generation notice: {e}")

@app.get("/")
async def root():
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": "/docs",
        "supported_languages": ["en", "hi", "ja"],
        "styles": {
            "indian": list(settings.INDIAN_STYLES.keys()),
            "japanese": list(settings.JAPANESE_STYLES.keys())
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "device": settings.DEVICE}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
