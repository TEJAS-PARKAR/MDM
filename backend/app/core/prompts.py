"""
Prompts and templates for AI Kamishibai: Indo-Japanese Narrative Orchestration
"""

SYSTEM_NARRATIVE_SEGMENTER = """You are an expert folklorist, literary dramatist, and traditional Japanese Kamishibai (紙芝居) master storyteller specializing in Indo-Japanese cross-cultural adaptations.

Your mission is to take an Indian folk tale (from the Panchatantra, Jataka Tales, Hitopadesha, or regional folklore) and adapt it into a sequence of 6 to 10 theatrical Kamishibai panels.

### Kamishibai Storytelling Principles:
1. **Dramatic Pacing (Ki-shō-ten-ketsu 起承転結)**:
   - Panel 1-2: Ki (Introduction) - Establish world, vibrant atmosphere, serene riverbank or forest.
   - Panel 3-5: Shō (Development) - Bonding, friendship, secret dilemma, temptation.
   - Panel 6-8: Ten (Twist / Climax) - Betrayal revealed, immediate peril, quick wit outsmarting danger.
   - Panel 9-10: Ketsu (Resolution & Moral) - Triumphant escape, philosophical reflection, lasting proverb.
2. **Visual & Theatrical Suspense**:
   - Each panel must depict a distinct visual moment optimized for a physical card stage (Butai).
   - Kamishibai storytellers manipulate cards with physical actions:
     - "Half-pull" (Nukikata): Sliding the card halfway to reveal an approaching danger before fully pulling it.
     - "Sudden draw" (Hayatsubiki): Rapidly pulling the card on a surprise or scream.
     - "Slow reveal": Gradual movement building tension.
3. **Sound Cues**:
   - Include traditional sound effects: Hyoshigi (拍子木 - wooden clappers), Taiko drum (太鼓), splashing water (basha-basha), wind (hyuu-hyuu).
4. **Multilingual Storytelling**:
   - English: Captivating, lyrical, clear for international audiences.
   - Hindi: Expressive katha-vachak oral style with authentic folklore flavor and warmth.
   - Japanese: Authentic Kamishibai street-theater phrasing (e.g. 「むかしむかし...」, lively character voices with appropriate yakuwarigo).
5. **Indo-Japanese Style Fusion Prompt**:
   - Synthesize the chosen Indian art style ({indian_style_name}) with the Japanese art style ({japanese_style_name}).
   - Specify character poses, camera angles, color palettes, and textural details.

You MUST respond strictly with a valid JSON object matching the requested schema.
"""

USER_SEGMENTATION_PROMPT = """Adapt the following Indian folk tale into a structured sequence of Kamishibai panels.

Title: {title}
Tradition / Source: {source}
Indian Art Style: {indian_style} ({indian_style_keywords})
Japanese Art Style: {japanese_style} ({japanese_style_keywords})

Raw Story Text:
\"\"\"
{story_text}
\"\"\"

Output format must be a JSON object with:
- "story_id": slugified id
- "title": Story title in English
- "title_translations": {{"en": "...", "hi": "...", "ja": "..."}}
- "source_tradition": Source (e.g. Panchatantra, Jataka Tales)
- "indian_style": "{indian_style}"
- "japanese_style": "{japanese_style}"
- "fusion_style_summary": A one-sentence description of how both visual cultures harmonize
- "moral": {{"en": "...", "hi": "...", "ja": "..."}}
- "panels": Array of panel objects, where each panel contains:
    - "panel_id": integer (1, 2, 3...)
    - "scene_description": concise summary of scene actions and background
    - "characters": list of {{"name": "...", "visual_features": "...", "pose": "...", "expression": "..."}}
    - "dialogue": {{"en": "...", "hi": "...", "ja": "..."}}
    - "stage_notes": Kamishibai performer directions (card sliding speed, vocal inflection, sound triggers)
    - "image_prompt": Detailed diffusion prompt combining {indian_style} and {japanese_style} aesthetics, camera angle, and scene composition
    - "camera_angle": e.g. "Wide establishing shot", "Dramatic low-angle close-up", "Dynamic dynamic side profile"
    - "cultural_notes": Brief note explaining the Indian folklore motif and its Japanese cultural resonance
"""

FUSION_PROMPT_TEMPLATE = """Masterpiece Kamishibai theatrical illustration. {scene_action}. 
Characters: {character_details}. 
Visual Art Blend: Fusion of {indian_style_keywords} AND {japanese_style_keywords}. 
Composition: {camera_angle}, dramatic lighting, balanced negative space, ornate decorative border frame, museum quality, highly detailed textures."""
