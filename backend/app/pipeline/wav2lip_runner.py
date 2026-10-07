"""
Wav2Lip Pipeline Runner for AI Kamishibai.
Synchronizes talking characters in static 2D panels with generated narration audio.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict
from PIL import Image, ImageDraw
from app.core.config import settings

class Wav2LipRunner:
    """
    Orchestrates Wav2Lip inference for animating character expressions and mouth movements
    in Kamishibai cards using the panel audio track.
    """

    def __init__(self):
        self.checkpoint_path = Path(os.getenv("WAV2LIP_CHECKPOINT", "backend/checkpoints/wav2lip_gan.pth"))
        self.face_detector = "s3fd"
        self.is_model_available = self.checkpoint_path.exists()

    def generate_lip_sync_video(
        self,
        image_path: Path,
        audio_path: Path,
        output_path: Path,
        fps: int = 25
    ) -> Dict[str, str]:
        """
        Executes Wav2Lip to generate a synchronized MP4 talking preview.
        Falls back to animated keyframe synthesis if deep model weights are not loaded.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.is_model_available:
            try:
                # Real Wav2Lip execution command
                cmd = [
                    "python", "inference.py",
                    "--checkpoint_path", str(self.checkpoint_path),
                    "--face", str(image_path),
                    "--audio", str(audio_path),
                    "--outfile", str(output_path),
                    "--fps", str(fps),
                    "--pads", "0", "10", "0", "0"
                ]
                print(f"[Wav2LipRunner] Running Wav2Lip inference: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if result.returncode == 0 and output_path.exists():
                    return {"status": "success", "video_path": str(output_path), "engine": "wav2lip"}
            except Exception as e:
                print(f"[Wav2LipRunner] Wav2Lip model inference encountered: {e}. Using animated keyframe fallback.")

        # Fallback: Keyframe animation synthesizing talking mouth cycle and subtle eye blink
        return self._generate_stylized_keyframe_clip(image_path, audio_path, output_path, fps=fps)

    def _generate_stylized_keyframe_clip(
        self,
        image_path: Path,
        audio_path: Path,
        output_path: Path,
        fps: int = 24
    ) -> Dict[str, str]:
        """
        Generates an animated MP4 preview using OpenCV and FFmpeg if available,
        or creates animated WebP/GIF frames.
        """
        try:
            import cv2
            import numpy as np

            # Load base image
            img_bgr = cv2.imread(str(image_path))
            if img_bgr is None:
                raise ValueError(f"Could not load image at {image_path}")

            h, w, _ = img_bgr.shape
            
            # Temporary video path without audio
            temp_vid = output_path.parent / f"temp_{output_path.stem}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            # Approximate 4 seconds video duration
            duration = 4.0
            total_frames = int(duration * fps)
            out = cv2.VideoWriter(str(temp_vid), fourcc, fps, (w, h))

            # Mouth center coordinate approximation
            mc_x, mc_y = int(w * 0.5), int(h * 0.52)

            for i in range(total_frames):
                frame = img_bgr.copy()
                
                # Rhythmic talking mouth aperture modulation
                cycle = (i % 8) / 8.0
                mouth_open = int(8 * abs(np.sin(cycle * np.pi)))
                
                # Draw subtle stylized mouth movement
                cv2.ellipse(frame, (mc_x, mc_y), (14, 4 + mouth_open), 0, 0, 360, (20, 20, 30), -1)
                
                # Occasional eye blink every ~40 frames
                if 38 <= (i % 50) <= 41:
                    cv2.line(frame, (mc_x - 30, mc_y - 40), (mc_x - 10, mc_y - 40), (20, 20, 30), 3)
                    cv2.line(frame, (mc_x + 10, mc_y - 40), (mc_x + 30, mc_y - 40), (20, 20, 30), 3)

                out.write(frame)
            out.release()

            # Merge audio if ffmpeg is available
            try:
                cmd = [
                    "ffmpeg", "-y", "-i", str(temp_vid), "-i", str(audio_path),
                    "-c:v", "libx264", "-c:a", "aac", "-shortest", str(output_path)
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
                if temp_vid.exists():
                    temp_vid.unlink()
            except Exception:
                # If ffmpeg is absent, rename temp video directly
                if temp_vid.exists():
                    shutil.move(str(temp_vid), str(output_path))

            return {"status": "success", "video_path": str(output_path), "engine": "procedural_animator"}

        except Exception as e:
            print(f"[Wav2LipRunner] Clip generation fallback: {e}")
            return {"status": "fallback_unavailable", "error": str(e)}

wav2lip_runner = Wav2LipRunner()
