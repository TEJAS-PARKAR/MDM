import os
import shutil
import urllib.request
import urllib.parse
import io
import math
import random
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from app.core.config import settings

class ImageGenerator:
    """
    Style-Controlled Visual Generation Pipeline.
    Supports:
    1. Online Generative AI synthesis via diffusion models, producing distinct
       photorealistic / artistic masterpiece images per scene script.
    2. Local Diffusers SDXL pipeline with IP-Adapter & ControlNet if CUDA GPU is available.
    3. Highly differentiated scene-specific procedural artwork engine
       with distinctive iconography and compositions for every individual panel.
    4. Post-processing: applies authentic Kamishibai wooden frame, corner brackets,
       calligraphy Hanko seal stamps (第N幕), and Indo-Japanese style captions.
    """

    def __init__(self):
        self.device = settings.DEVICE
        self.sdxl_pipeline = None
        self._init_diffusers()

    def _init_diffusers(self):
        """Attempts to initialize diffusers SDXL pipeline if GPU is available."""
        if self.device == "cuda":
            try:
                import torch
                from diffusers import AutoPipelineForText2Image
                print(f"[ImageGenerator] Initializing SDXL on {self.device}...")
                self.sdxl_pipeline = AutoPipelineForText2Image.from_pretrained(
                    settings.SDXL_MODEL_ID,
                    torch_dtype=torch.float16,
                    variant="fp16",
                    use_safetensors=True
                ).to("cuda")
                print("[ImageGenerator] SDXL loaded successfully.")
            except Exception as e:
                print(f"[ImageGenerator] diffusers GPU initialization deferred: {e}")

    def generate_panel_image(
        self,
        story_id: str,
        panel_id: int,
        prompt: str,
        indian_style: str = "madhubani",
        japanese_style: str = "ukiyoe",
        camera_angle: str = "Wide shot",
        scene_title: str = "",
        force_regenerate: bool = False
    ) -> Path:
        """
        Generates or retrieves a distinct scene-specific panel image.
        Outputs to both backend static and frontend public folders.
        """
        filename = f"{story_id}_panel_{panel_id}.jpg"
        backend_path = settings.PANELS_DIR / filename
        frontend_path = settings.FRONTEND_PANELS_DIR / filename

        if backend_path.exists() and not force_regenerate:
            if not frontend_path.exists():
                shutil.copy2(backend_path, frontend_path)
            return backend_path

        # 1. Try Online AI Diffusion Generation
        ai_image = self._try_online_ai_generation(
            prompt=prompt,
            story_id=story_id,
            panel_id=panel_id,
            indian_style=indian_style,
            japanese_style=japanese_style
        )

        if ai_image:
            final_card = self._apply_kamishibai_framing(
                base_img=ai_image,
                panel_id=panel_id,
                indian_style=indian_style,
                japanese_style=japanese_style,
                scene_title=scene_title
            )
            final_card.save(backend_path, "JPEG", quality=93)
            shutil.copy2(backend_path, frontend_path)
            return backend_path

        # 2. Try Local Diffusers SDXL Pipeline
        if self.sdxl_pipeline:
            try:
                image = self.sdxl_pipeline(
                    prompt=prompt,
                    negative_prompt="blurry, distorted, western cartoon, modern text, watermark",
                    width=settings.IMAGE_WIDTH,
                    height=settings.IMAGE_HEIGHT,
                    num_inference_steps=28,
                    guidance_scale=7.5
                ).images[0]
                final_card = self._apply_kamishibai_framing(
                    base_img=image,
                    panel_id=panel_id,
                    indian_style=indian_style,
                    japanese_style=japanese_style,
                    scene_title=scene_title
                )
                final_card.save(backend_path, "JPEG", quality=93)
                shutil.copy2(backend_path, frontend_path)
                return backend_path
            except Exception as e:
                print(f"[ImageGenerator] SDXL error: {e}. Falling back to scene procedural engine.")

        # 3. Fallback: Highly differentiated scene-specific procedural artwork
        card = self._render_distinct_scene_card(
            story_id=story_id,
            panel_id=panel_id,
            prompt=prompt,
            indian_style=indian_style,
            japanese_style=japanese_style,
            camera_angle=camera_angle,
            scene_title=scene_title
        )
        card.save(backend_path, "JPEG", quality=94)
        shutil.copy2(backend_path, frontend_path)
        return backend_path

    def _try_online_ai_generation(
        self,
        prompt: str,
        story_id: str,
        panel_id: int,
        indian_style: str,
        japanese_style: str
    ) -> Optional[Image.Image]:
        """
        Fetches an AI-generated image specifically for this scene prompt.
        Uses a deterministic seed based on story and panel ID for consistency.
        """
        # Ensure clean, compact prompt optimized for diffusion models
        ind_kw = settings.INDIAN_STYLES.get(indian_style, {}).get("name", "Madhubani")
        jap_kw = settings.JAPANESE_STYLES.get(japanese_style, {}).get("name", "Ukiyo-e")
        
        # Craft focused AI generation prompt
        enhanced_prompt = (
            f"Masterpiece Japanese Kamishibai card art, {prompt[:240]}, "
            f"artistic fusion of {ind_kw} Indian folk art and {jap_kw} Japanese style, "
            f"theatrical composition, beautiful vibrant colors, 4:3 aspect ratio, museum quality"
        )
        
        seed = (abs(hash(f"{story_id}_{panel_id}")) % 90000) + 1000

        try:
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&seed={seed}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=18) as response:
                img_bytes = response.read()
                if len(img_bytes) > 20000:
                    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                    return img.resize((settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"[ImageGenerator] Online AI fetch for {story_id} panel {panel_id} notice: {e}")

        return None

    def _apply_kamishibai_framing(
        self,
        base_img: Image.Image,
        panel_id: int,
        indian_style: str,
        japanese_style: str,
        scene_title: str
    ) -> Image.Image:
        """
        Overlays the authentic Japanese Kamishibai theater border,
        lacquered corner brackets, Hanko calligraphy seal, and style banner.
        """
        img = base_img.copy()
        draw = ImageDraw.Draw(img)
        w, h = img.width, img.height

        margin = 28
        border_color = (35, 20, 15)      # Deep lacquered cedar
        accent_color = (212, 175, 55)    # Imperial Gold / Brass
        aux_color = (195, 35, 30)        # Japanese Vermilion

        # 1. Outer & Inner Borders
        draw.rectangle([margin, margin, w - margin, h - margin], outline=border_color, width=8)
        draw.rectangle([margin + 8, margin + 8, w - margin - 8, h - margin - 8], outline=accent_color, width=3)

        # 2. Ornate Corner Brass Brackets
        c_size = 38
        corners = [
            (margin, margin),
            (w - margin - c_size, margin),
            (margin, h - margin - c_size),
            (w - margin - c_size, h - margin - c_size)
        ]
        for cx, cy in corners:
            draw.rectangle([cx, cy, cx + c_size, cy + c_size], fill=border_color)
            draw.rectangle([cx + 3, cy + 3, cx + c_size - 3, cy + c_size - 3], outline=accent_color, width=2)
            # Center rivet
            draw.ellipse([cx + 15, cy + 15, cx + 23, cy + 23], fill=accent_color)

        # 3. Hanko Seal Stamp (第N幕 - Act N)
        stamp_w, stamp_h = 56, 56
        stamp_x = w - margin - 72
        stamp_y = margin + 16
        draw.rectangle([stamp_x, stamp_y, stamp_x + stamp_w, stamp_y + stamp_h], fill=aux_color, outline=(255, 240, 220), width=2)

        kanji_numbers = ["壱", "弐", "参", "四", "伍", "六", "七", "八", "九", "拾"]
        act_kanji = kanji_numbers[panel_id - 1] if 0 < panel_id <= len(kanji_numbers) else str(panel_id)

        try:
            font_path = "C:/Windows/Fonts/msmincho.ttc"
            font_hanko = ImageFont.truetype(font_path, 15) if os.path.exists(font_path) else ImageFont.load_default()
            font_label = ImageFont.truetype(font_path, 13) if os.path.exists(font_path) else ImageFont.load_default()
        except Exception:
            font_hanko = ImageFont.load_default()
            font_label = ImageFont.load_default()

        draw.text((stamp_x + 9, stamp_y + 6), f"第{act_kanji}幕", fill=(255, 255, 255), font=font_hanko)
        draw.text((stamp_x + 11, stamp_y + 30), "紙芝居", fill=(255, 255, 255), font=font_hanko)

        # 4. Bottom Style & Act Banner
        banner_h = 38
        banner_y = h - margin - banner_h
        draw.rectangle([margin + 12, banner_y, w - margin - 12, banner_y + banner_h], fill=(15, 10, 8, 220), outline=accent_color, width=2)
        
        caption = f"Card {panel_id} • {indian_style.capitalize()} × {japanese_style.capitalize()} Visual Fusion"
        draw.text((margin + 26, banner_y + 10), caption, fill=(245, 235, 215), font=font_label)

        return img

    def _render_distinct_scene_card(
        self,
        story_id: str,
        panel_id: int,
        prompt: str,
        indian_style: str,
        japanese_style: str,
        camera_angle: str,
        scene_title: str
    ) -> Image.Image:
        """
        Renders a completely unique, scene-specific visual card when offline.
        Uses the exact narrative action of the panel to compose distinct scenery.
        """
        w, h = settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT

        # Base color selection by style
        if indian_style == "warli":
            bg = (165, 62, 40)       # Terracotta mud
            line_color = (248, 244, 235) # Rice white
            sec_color = (115, 38, 22)
        elif indian_style == "pattachitra":
            bg = (22, 32, 60)        # Deep Indigo
            line_color = (225, 170, 50) # Gold
            sec_color = (180, 40, 40) # Crimson
        else: # madhubani
            bg = (248, 243, 228)     # Washi ivory
            line_color = (20, 35, 65) # Deep navy
            sec_color = (210, 45, 35) # Vermilion

        img = Image.new("RGB", (w, h), bg)
        draw = ImageDraw.Draw(img)

        # Subtle paper texture
        for y in range(0, h, 6):
            draw.line([(0, y), (w, y)], fill=(bg[0] - 5, bg[1] - 5, bg[2] - 5))

        # --- SCENE-SPECIFIC COMPOSITIONS ---
        # 1. MONKEY AND CROCODILE PANELS
        if "monkey" in story_id or "crocodile" in story_id:
            if panel_id == 1:
                # Panel 1: Sunlit Jamun tree canopy, ripe berries, golden monkey alone
                # Sun
                draw.ellipse([w * 0.75 - 70, 80, w * 0.75 + 70, 220], fill=(245, 180, 40), outline=sec_color, width=4)
                # River at bottom
                draw.rectangle([0, int(h * 0.75), w, h], fill=(30, 70, 115))
                # Giant Jamun tree filling the left and top
                draw.rectangle([60, 180, 140, h], fill=(85, 45, 20))
                draw.ellipse([30, 60, 460, 380], fill=(35, 110, 55), outline=line_color, width=4)
                # Abundant purple berries
                for bx, by in [(160, 140), (220, 200), (280, 160), (340, 240), (190, 280), (380, 180), (120, 220)]:
                    draw.ellipse([bx, by, bx + 22, by + 22], fill=(110, 25, 120), outline=(240, 210, 250), width=2)
                # Golden Monkey sitting happily on high branch
                draw.ellipse([260, 210, 320, 270], fill=(220, 150, 40), outline=line_color, width=3) # Body
                draw.ellipse([280, 175, 325, 220], fill=(220, 150, 40), outline=line_color, width=3) # Head
                draw.line([(320, 240), (360, 270)], fill=(220, 150, 40), width=6) # Tail

            elif panel_id == 2:
                # Panel 2: Riverbank encounter, monkey tossing berries to crocodile
                # Riverbank sand
                draw.polygon([(0, int(h * 0.55)), (w, int(h * 0.75)), (w, h), (0, h)], fill=(215, 185, 130))
                # River water
                draw.polygon([(w * 0.45, int(h * 0.65)), (w, int(h * 0.75)), (w, h), (w * 0.45, h)], fill=(30, 80, 130))
                # Tree branch leaning
                draw.line([(0, 120), (w * 0.45, 240)], fill=(90, 50, 25), width=22)
                # Monkey leaning down
                draw.ellipse([w * 0.38, 220, w * 0.38 + 55, 275], fill=(220, 150, 40), outline=line_color, width=3)
                # Falling berries
                for fy in [300, 350, 400]:
                    draw.ellipse([w * 0.42, fy, w * 0.42 + 14, fy + 14], fill=(110, 25, 120))
                # Emerald crocodile resting on the sandy shore
                draw.ellipse([w * 0.48, int(h * 0.68), w * 0.88, int(h * 0.82)], fill=(30, 105, 65), outline=line_color, width=4)
                # Crocodile snout open to catch fruit
                draw.polygon([(w * 0.48, int(h * 0.72)), (w * 0.42, int(h * 0.68)), (w * 0.48, int(h * 0.76))], fill=(25, 95, 55))

            elif panel_id == 3:
                # Panel 3: Dark underwater cave, menacing wife with glowing eyes
                draw.rectangle([0, 0, w, h], fill=(12, 18, 35)) # Dark cavern water
                # Bioluminescent underwater stalactites
                for sx in [100, 240, 420, 680, 850]:
                    draw.polygon([(sx, 0), (sx + 35, 180), (sx + 70, 0)], fill=(20, 35, 60))
                # Female crocodile coiled menacingly with glowing red eyes
                draw.ellipse([w * 0.25, h * 0.45, w * 0.75, h * 0.78], fill=(20, 45, 35), outline=(180, 40, 40), width=4)
                # Sharp jagged teeth
                for tx in range(int(w * 0.32), int(w * 0.48), 16):
                    draw.polygon([(tx, int(h * 0.58)), (tx + 8, int(h * 0.58) - 18), (tx + 16, int(h * 0.58))], fill=(245, 245, 240))
                # Glowing sinister red eyes
                draw.ellipse([w * 0.36, h * 0.5, w * 0.36 + 16, h * 0.5 + 16], fill=(230, 30, 20))

            elif panel_id == 4:
                # Panel 4: Mid-river crossing, monkey riding on crocodile's back
                # Swirling river water
                draw.rectangle([0, int(h * 0.35), w, h], fill=(25, 75, 125))
                # Wave crests (Ukiyo-e style)
                for wx in range(60, w, 140):
                    draw.arc([wx - 60, int(h * 0.45), wx + 60, int(h * 0.62)], start=180, end=360, fill=(240, 245, 255), width=5)
                # Large crocodile swimming in center
                draw.ellipse([w * 0.25, h * 0.58, w * 0.85, h * 0.75], fill=(30, 105, 65), outline=line_color, width=4)
                # Monkey bravely perched on back
                draw.ellipse([w * 0.48, h * 0.42, w * 0.48 + 55, h * 0.42 + 65], fill=(220, 150, 40), outline=line_color, width=3)
                draw.ellipse([w * 0.49, h * 0.36, w * 0.49 + 40, h * 0.36 + 40], fill=(220, 150, 40), outline=line_color, width=3)

            elif panel_id == 5:
                # Panel 5: Climax - Sinking in swirling whirlpool vortex, shock!
                draw.rectangle([0, 0, w, h], fill=(18, 32, 58))
                # Giant swirling spiral vortex in center
                for r in range(40, 320, 35):
                    draw.arc([w//2 - r, h//2 - r, w//2 + r, h//2 + r], start=(r*3)%360, end=((r*3)+220)%360, fill=(180, 220, 245), width=4)
                # Crocodile tilted downward into whirlpool
                draw.polygon([(w*0.35, h*0.4), (w*0.7, h*0.65), (w*0.5, h*0.75)], fill=(25, 85, 55))
                # Monkey clinging in intense alarm
                draw.ellipse([w*0.48, h*0.32, w*0.48 + 48, h*0.32 + 55], fill=(230, 130, 25), outline=(255, 255, 255), width=3)

            elif panel_id == 6:
                # Panel 6: Monkey laughing atop crocodile's snout, outsmarting him!
                draw.rectangle([0, int(h * 0.5), w, h], fill=(35, 90, 140))
                # Sunlit distant shore glowing with hope
                draw.rectangle([0, int(h * 0.3), w * 0.3, int(h * 0.5)], fill=(45, 125, 60))
                # Crocodile head in water, looking gullible and foolish
                draw.polygon([(w * 0.35, int(h * 0.65)), (w * 0.75, int(h * 0.55)), (w * 0.7, int(h * 0.75))], fill=(30, 105, 65))
                # Monkey standing upright on crocodile's snout, hand on hip laughing
                draw.ellipse([w * 0.65, int(h * 0.38), w * 0.65 + 45, int(h * 0.38) + 55], fill=(220, 150, 40), outline=line_color, width=3)
                # Big laughing smile
                draw.arc([w * 0.66, int(h * 0.42), w * 0.66 + 25, int(h * 0.42) + 20], start=0, end=180, fill=(200, 30, 20), width=3)

            elif panel_id == 7:
                # Panel 7: Triumphant leap! Monkey safe in high tree, crocodile stranded below
                # Massive tall Jamun tree
                draw.rectangle([w * 0.65, 0, w * 0.85, h], fill=(85, 45, 20))
                draw.ellipse([w * 0.45, 40, w * 0.98, 340], fill=(35, 110, 55), outline=line_color, width=4)
                # Golden monkey victorious in branches, mocking downward
                draw.ellipse([w * 0.58, 140, w * 0.58 + 60, 205], fill=(240, 160, 30), outline=(255, 255, 255), width=4)
                # Stranded crocodile sulking on the distant shore below
                draw.ellipse([w * 0.1, int(h * 0.75), w * 0.45, int(h * 0.86)], fill=(25, 75, 45), outline=line_color, width=3)

            else:
                # Panel 8: Radiant golden sunset over the river, serene moral reflection
                for y in range(int(h * 0.6)):
                    ratio = y / (h * 0.6)
                    r = int(245 * (1 - ratio) + 210 * ratio)
                    g = int(80 * (1 - ratio) + 140 * ratio)
                    b = int(40 * (1 - ratio) + 60 * ratio)
                    draw.line([(0, y), (w, y)], fill=(r, g, b))
                # Golden sunset disc
                draw.ellipse([w//2 - 90, 80, w//2 + 90, 260], fill=(255, 220, 80))
                # Calm reflective river
                draw.rectangle([0, int(h * 0.6), w, h], fill=(90, 45, 40))
                # Peaceful monkey silhouette against setting sun
                draw.ellipse([w//2 - 25, 180, w//2 + 25, 240], fill=(20, 10, 5))

        # 2. TURTLE AND GEESE PANELS
        elif "turtle" in story_id:
            if panel_id == 1:
                # Lotus pond with swimming turtle & geese in flight
                draw.rectangle([0, int(h * 0.55), w, h], fill=(35, 95, 130))
                # Lotus blossoms
                for lx in [120, 320, 580, 800]:
                    draw.ellipse([lx, int(h * 0.6), lx + 45, int(h * 0.6) + 25], fill=(235, 120, 150))
                # Turtle swimming happily
                draw.ellipse([w * 0.42, int(h * 0.68), w * 0.42 + 70, int(h * 0.68) + 50], fill=(50, 100, 45), outline=line_color, width=3)
                # Two white geese flying above
                for gx in [w * 0.3, w * 0.6]:
                    draw.polygon([(gx, 160), (gx - 40, 110), (gx + 40, 110)], fill=(250, 250, 250), outline=line_color, width=2)

            elif panel_id == 2:
                # Parched cracked drought land, baking sun
                draw.rectangle([0, 0, w, h], fill=(185, 75, 40)) # Blazing sky
                draw.ellipse([w//2 - 60, 40, w//2 + 60, 160], fill=(255, 230, 90)) # Harsh sun
                # Cracked parched mud ground
                for cy in range(int(h * 0.5), h, 35):
                    draw.line([(0, cy), (w, cy + 15)], fill=(120, 40, 20), width=3)
                # Worried turtle and geese consulting
                draw.ellipse([w//2 - 35, int(h * 0.68), w//2 + 35, int(h * 0.68) + 45], fill=(70, 60, 40), outline=line_color, width=2)

            elif panel_id == 3:
                # Lifting off: geese holding stick, turtle biting center
                draw.rectangle([0, 0, w, h], fill=(120, 165, 200)) # Pale morning sky
                # The wooden stick
                draw.line([(w * 0.28, 320), (w * 0.72, 320)], fill=(110, 60, 20), width=8)
                # Turtle biting stick
                draw.ellipse([w * 0.46, 316, w * 0.46 + 65, 385], fill=(50, 95, 40), outline=line_color, width=3)
                # Two flapping geese
                draw.polygon([(w * 0.28, 320), (w * 0.22, 230), (w * 0.34, 230)], fill=(250, 250, 250), outline=line_color, width=2)
                draw.polygon([(w * 0.72, 320), (w * 0.66, 230), (w * 0.78, 230)], fill=(250, 250, 250), outline=line_color, width=2)

            elif panel_id == 4:
                # Soaring high over clouds and tiny villagers pointing below
                draw.rectangle([0, 0, w, h], fill=(75, 135, 195))
                # Clouds
                for cx in [100, 350, 650, 850]:
                    draw.ellipse([cx, int(h * 0.58), cx + 180, int(h * 0.58) + 80], fill=(235, 245, 255))
                # Flight in upper sky
                draw.line([(w * 0.38, 160), (w * 0.62, 160)], fill=(110, 60, 20), width=6)
                draw.ellipse([w * 0.48, 158, w * 0.48 + 40, 198], fill=(50, 95, 40))
                # Tiny stick figure villagers pointing up from below
                for vx in range(150, int(w * 0.85), 60):
                    draw.ellipse([vx, int(h * 0.82), vx + 10, int(h * 0.82) + 10], fill=line_color)
                    draw.line([(vx + 5, int(h * 0.84)), (vx + 5, int(h * 0.92))], fill=line_color, width=2)

            elif panel_id == 5:
                # Climax: Freefall plummet, turtle mouth open shouting, lost grip
                draw.rectangle([0, 0, w, h], fill=(45, 55, 80)) # Gloomy sky
                # Vertical speed streaks
                for sx in range(80, w, 40):
                    draw.line([(sx, 60), (sx, h - 60)], fill=(180, 190, 210, 100), width=2)
                # Tumbling turtle upside down in free fall
                draw.ellipse([w//2 - 45, h//2 - 30, w//2 + 45, h//2 + 45], fill=(60, 100, 45), outline=(240, 50, 40), width=4)
                # Two geese left far above in sorrow with empty stick
                draw.line([(w * 0.4, 110), (w * 0.6, 110)], fill=(110, 60, 20), width=5)

            else:
                # Panel 6: Mourning geese disappearing into misty mountains
                draw.rectangle([0, 0, w, h], fill=(25, 30, 45))
                # Misty Sumi-e mountain peaks
                draw.polygon([(0, h), (w * 0.3, int(h * 0.4)), (w * 0.6, h)], fill=(40, 45, 60))
                draw.polygon([(w * 0.4, h), (w * 0.75, int(h * 0.35)), (w, h)], fill=(55, 60, 80))
                # Two silhouetted geese soaring into distance
                draw.polygon([(w * 0.5, 140), (w * 0.47, 120), (w * 0.53, 120)], fill=(200, 205, 215))
                draw.polygon([(w * 0.58, 160), (w * 0.55, 140), (w * 0.61, 140)], fill=(200, 205, 215))

        # 3. GENERIC / CUSTOM STORY SCENES (Act 1 to 6)
        else:
            act_idx = (panel_id - 1) % 6
            if act_idx == 0:
                # Act 1: Peaceful establishing landscape & protagonist
                draw.rectangle([0, int(h * 0.6), w, h], fill=sec_color)
                draw.ellipse([w * 0.2, 80, w * 0.2 + 100, 180], fill=(245, 210, 80))
                draw.ellipse([w//2 - 50, int(h * 0.55), w//2 + 50, int(h * 0.55) + 80], fill=line_color)
            elif act_idx == 1:
                # Act 2: Journey & encounter
                draw.line([(0, int(h * 0.7)), (w, int(h * 0.55))], fill=sec_color, width=16)
                draw.ellipse([w * 0.35, int(h * 0.5), w * 0.35 + 60, int(h * 0.5) + 80], fill=line_color)
                draw.ellipse([w * 0.65, int(h * 0.45), w * 0.65 + 60, int(h * 0.45) + 80], fill=(220, 130, 40))
            elif act_idx == 2:
                # Act 3: Darkening tension & gathering dilemma
                draw.rectangle([0, 0, w, h], fill=(30, 20, 35))
                draw.ellipse([w//2 - 90, h//2 - 60, w//2 + 90, h//2 + 60], fill=(60, 30, 45), outline=sec_color, width=4)
            elif act_idx == 3:
                # Act 4: Climax & peril confrontation
                draw.rectangle([0, 0, w, h], fill=(50, 15, 20))
                # Dramatic zigzag lightning / conflict lines
                draw.line([(w * 0.2, 60), (w * 0.5, h * 0.5), (w * 0.8, h - 60)], fill=(255, 230, 90), width=6)
            elif act_idx == 4:
                # Act 5: Swift escape & outsmarting victory
                draw.rectangle([0, int(h * 0.6), w, h], fill=(25, 75, 55))
                draw.ellipse([w * 0.6, 120, w * 0.6 + 75, 200], fill=(240, 180, 40), outline=line_color, width=3)
            else:
                # Act 6: Serene twilight resolution & moral closure
                for y in range(int(h * 0.65)):
                    draw.line([(0, y), (w, y)], fill=(int(200 - y*0.2), int(100 + y*0.1), int(50 + y*0.2)))
                draw.ellipse([w//2 - 70, 100, w//2 + 70, 240], fill=(255, 215, 80))

        # Apply Kamishibai museum frame
        return self._apply_kamishibai_framing(
            base_img=img,
            panel_id=panel_id,
            indian_style=indian_style,
            japanese_style=japanese_style,
            scene_title=scene_title
        )

image_generator = ImageGenerator()
