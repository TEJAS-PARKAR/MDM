import asyncio
import os
import shutil
import math
import struct
import wave
from pathlib import Path
from typing import Dict, Optional
from app.core.config import settings

class TTSGenerator:
    """
    Multilingual Audio Narration Engine for AI Kamishibai.
    Generates emotive voiceovers in English, Hindi, and Japanese
    using high-fidelity neural speech (edge-tts) with graceful fallback.
    """

    def __init__(self):
        self.voices = {
            "en": "en-US-ChristopherNeural",
            "hi": "hi-IN-MadhurNeural",
            "ja": "ja-JP-NanamiNeural"
        }
        self._ensure_sound_effects()

    async def synthesize_speech_async(
        self,
        text: str,
        lang: str,
        story_id: str,
        panel_id: int,
        voice_rate: str = "+0%",
        voice_pitch: str = "+0Hz",
        force_regenerate: bool = False
    ) -> Path:
        """
        Synthesizes speech for a given panel dialogue in the chosen language.
        Saves to backend static and syncs to frontend public directory.
        """
        filename = f"{story_id}_panel_{panel_id}_{lang}.mp3"
        backend_path = settings.AUDIO_DIR / filename
        frontend_path = settings.FRONTEND_AUDIO_DIR / filename

        if backend_path.exists() and not force_regenerate:
            if not frontend_path.exists():
                shutil.copy2(backend_path, frontend_path)
            return backend_path

        voice = self.voices.get(lang, self.voices["en"])

        # 1. Attempt edge-tts neural generation
        try:
            import edge_tts
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=voice_rate,
                pitch=voice_pitch
            )
            await communicate.save(str(backend_path))
            
            # Verify file has non-zero size
            if backend_path.exists() and backend_path.stat().st_size > 500:
                shutil.copy2(backend_path, frontend_path)
                return backend_path
        except Exception as e:
            print(f"[TTSGenerator] edge-tts error for {lang}: {e}. Utilizing acoustic fallback.")

        # 2. Fallback: Generate an authentic acoustic waveform file
        wav_filename = f"{story_id}_panel_{panel_id}_{lang}.wav"
        backend_wav = settings.AUDIO_DIR / wav_filename
        frontend_wav = settings.FRONTEND_AUDIO_DIR / wav_filename
        self._generate_synthetic_narration_tone(backend_wav, duration_sec=4.0, lang=lang)
        shutil.copy2(backend_wav, frontend_wav)
        
        # Also copy as mp3 name for URL consistency if needed
        shutil.copy2(backend_wav, backend_path)
        shutil.copy2(backend_wav, frontend_path)
        return backend_path

    def synthesize_speech(
        self,
        text: str,
        lang: str,
        story_id: str,
        panel_id: int,
        force_regenerate: bool = False
    ) -> Path:
        """Synchronous wrapper for synthesize_speech_async."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # In nested event loop, create a new one or use thread runner
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    return pool.submit(
                        asyncio.run,
                        self.synthesize_speech_async(text, lang, story_id, panel_id, force_regenerate=force_regenerate)
                    ).result()
            else:
                return loop.run_until_complete(
                    self.synthesize_speech_async(text, lang, story_id, panel_id, force_regenerate=force_regenerate)
                )
        except Exception:
            return asyncio.run(
                self.synthesize_speech_async(text, lang, story_id, panel_id, force_regenerate=force_regenerate)
            )

    async def batch_synthesize_story(self, story_data, force_regenerate: bool = False) -> Dict[str, Dict[int, str]]:
        """Synthesizes all panels for all 3 languages (EN, HI, JA)."""
        results = {"en": {}, "hi": {}, "ja": {}}
        story_id = story_data.story_id

        tasks = []
        for panel in story_data.panels:
            for lang, text in [("en", panel.dialogue.en), ("hi", panel.dialogue.hi), ("ja", panel.dialogue.ja)]:
                tasks.append((panel.panel_id, lang, text))

        for panel_id, lang, text in tasks:
            try:
                path = await self.synthesize_speech_async(
                    text=text,
                    lang=lang,
                    story_id=story_id,
                    panel_id=panel_id,
                    force_regenerate=force_regenerate
                )
                results[lang][panel_id] = f"/audio/{path.name}"
            except Exception as e:
                print(f"[TTSGenerator] Failed to synthesize panel {panel_id} {lang}: {e}")

        return results

    def _ensure_sound_effects(self):
        """Generates authentic traditional sound effects (Hyoshigi clappers, Taiko drum, Wind chime)."""
        # Hyoshigi Clappers (拍子木): Sharp resonant wooden clicks
        hyoshigi_path = settings.AUDIO_DIR / "hyoshigi.wav"
        if not hyoshigi_path.exists():
            self._generate_hyoshigi_clapper(hyoshigi_path)
        front_hyoshigi = settings.FRONTEND_AUDIO_DIR / "hyoshigi.wav"
        if not front_hyoshigi.exists() and hyoshigi_path.exists():
            shutil.copy2(hyoshigi_path, front_hyoshigi)

        # Taiko Drum (太鼓): Low deep percussive resonance
        taiko_path = settings.AUDIO_DIR / "taiko.wav"
        if not taiko_path.exists():
            self._generate_taiko_drum(taiko_path)
        front_taiko = settings.FRONTEND_AUDIO_DIR / "taiko.wav"
        if not front_taiko.exists() and taiko_path.exists():
            shutil.copy2(taiko_path, front_taiko)

        # Paper slide sound (紙引き): Mimics traditional paper sliding out of wooden Butai
        slide_path = settings.AUDIO_DIR / "paper_slide.wav"
        if not slide_path.exists():
            self._generate_paper_slide(slide_path)
        front_slide = settings.FRONTEND_AUDIO_DIR / "paper_slide.wav"
        if not front_slide.exists() and slide_path.exists():
            shutil.copy2(slide_path, front_slide)

    def _generate_hyoshigi_clapper(self, file_path: Path):
        """Generates traditional Japanese wooden clapper sound (Chon-Chon)."""
        sample_rate = 44100
        duration = 1.2
        num_samples = int(sample_rate * duration)
        
        with wave.open(str(file_path), "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            frames = bytearray()
            # Two distinct wooden clicks: at 0.1s and 0.5s
            for i in range(num_samples):
                t = i / sample_rate
                val = 0.0
                
                # First click (Chon!)
                if 0.05 <= t <= 0.35:
                    dt = t - 0.05
                    envelope = math.exp(-35 * dt)
                    # Resonant wooden frequency blend: 850Hz, 1700Hz, 2550Hz
                    val += (0.6 * math.sin(2 * math.pi * 850 * dt) + 
                            0.3 * math.sin(2 * math.pi * 1700 * dt) +
                            0.1 * math.sin(2 * math.pi * 2550 * dt)) * envelope
                
                # Second click (Chon!)
                if 0.45 <= t <= 0.85:
                    dt = t - 0.45
                    envelope = math.exp(-32 * dt)
                    val += (0.65 * math.sin(2 * math.pi * 880 * dt) + 
                            0.25 * math.sin(2 * math.pi * 1760 * dt) +
                            0.1 * math.sin(2 * math.pi * 2600 * dt)) * envelope
                
                clamped = max(-1.0, min(1.0, val))
                sample_int = int(clamped * 32767)
                frames.extend(struct.pack("<h", sample_int))
            wav.writeframes(frames)

    def _generate_taiko_drum(self, file_path: Path):
        """Generates traditional Japanese Taiko drum boom (Don!)."""
        sample_rate = 44100
        duration = 1.8
        num_samples = int(sample_rate * duration)
        
        with wave.open(str(file_path), "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            frames = bytearray()
            for i in range(num_samples):
                t = i / sample_rate
                val = 0.0
                if 0.05 <= t <= 1.5:
                    dt = t - 0.05
                    envelope = math.exp(-4 * dt)
                    # Low punch 65Hz sliding down to 48Hz
                    freq = 65.0 - (15.0 * dt)
                    val = 0.9 * math.sin(2 * math.pi * freq * dt) * envelope
                
                clamped = max(-1.0, min(1.0, val))
                sample_int = int(clamped * 32767)
                frames.extend(struct.pack("<h", sample_int))
            wav.writeframes(frames)

    def _generate_paper_slide(self, file_path: Path):
        """Generates physical paper sliding sound (whispering friction against wood)."""
        sample_rate = 44100
        duration = 0.8
        num_samples = int(sample_rate * duration)
        
        with wave.open(str(file_path), "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            frames = bytearray()
            import random
            for i in range(num_samples):
                t = i / sample_rate
                # Friction noise modulated by bell curve envelope
                envelope = math.sin(math.pi * (t / duration)) ** 2
                noise = (random.random() * 2 - 1) * 0.25
                # Filtered hiss
                val = noise * envelope
                clamped = max(-1.0, min(1.0, val))
                sample_int = int(clamped * 32767)
                frames.extend(struct.pack("<h", sample_int))
            wav.writeframes(frames)

    def _generate_synthetic_narration_tone(self, file_path: Path, duration_sec: float = 3.5, lang: str = "en"):
        """Generates a pleasant melodic chime indicating narration for offline fallback."""
        sample_rate = 44100
        num_samples = int(sample_rate * duration_sec)
        
        # Pitches by language: Japanese (pentatonic), Hindi (raga tone), English (warm fourth)
        base_freq = 330.0 if lang == "ja" else (293.66 if lang == "hi" else 261.63)
        
        with wave.open(str(file_path), "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            
            frames = bytearray()
            for i in range(num_samples):
                t = i / sample_rate
                envelope = math.exp(-1.5 * (t % 1.2))
                val = (0.5 * math.sin(2 * math.pi * base_freq * t) + 
                       0.3 * math.sin(2 * math.pi * (base_freq * 1.5) * t)) * envelope
                clamped = max(-1.0, min(1.0, val))
                sample_int = int(clamped * 32767)
                frames.extend(struct.pack("<h", sample_int))
            wav.writeframes(frames)

tts_generator = TTSGenerator()
