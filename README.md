# 🎭 AI Kamishibai: Indo-Japanese Cross-Cultural Visual Storytelling Platform

> **Where Indian Folklore Meets Traditional Japanese Street-Theater & Anime Artistry**  
> An automated generative AI pipeline and interactive web application adapting ancient Indian folk tales (*Panchatantra, Jataka Tales*) into the traditional Japanese Kamishibai (紙芝居 - "paper play") format with trilingual neural audio in **English, हिन्दी (Hindi), and 日本語 (Japanese)**.

---

## 🌟 Key Features

1. **Digital Butai (舞台) Interactive Stage**:
   - Authentic Japanese wooden theater stage with dark cedar wood grain and ornamental brass brackets.
   - Traditional 3D folding doors (*Tobira* / 扉) that open with ceremonial **Hyoshigi (拍子木)** wooden clappers sound.
   - **Horizontal Card Sliding**: Smooth physical animation mimicking sliding illustrated paper cards out of a wooden frame, complete with paper friction sound.
   - **Nukikata (抜き方 / Half-Pull)**: Dedicated theatrical suspense button to pull cards 45% out to tease climaxes.

2. **Multilingual Audio Narration Engine**:
   - Neural speech synthesis in 3 languages:
     - 🇬🇧 **English**: Warm, lyrical storytelling (`en-US-ChristopherNeural` / `en-IN-PrabhatNeural`)
     - 🇮🇳 **हिन्दी**: Expressive oral katha-vachak cadence (`hi-IN-MadhurNeural` / `hi-IN-SwaraNeural`)
     - 🇯🇵 **日本語**: Authentic street-theater narrator cadence (`ja-JP-NanamiNeural`)
   - Dynamic real-time language toggling without disrupting visual stage position or re-triggering card jumps.
   - Auto-play story mode advancing cards synchronized with audio narration.

3. **Indo-Japanese Cross-Cultural Style Synthesis Matrix**:
   - **Indian Folk Traditions**:
     - *Madhubani (Mithila)*: Intricate double black outlines, floral geometries, and natural mineral dyes.
     - *Warli Tribal*: Terracotta red clay background with white rice pigment stick figures and Tarpa circles.
     - *Pattachitra*: Odisha scroll paintings with bold contour lines and ornate mythological borders.
   - **Japanese Art Traditions**:
     - *Ukiyo-e*: Edo woodblock prints, Hokusai wave foam, and subtle bokashi gradients.
     - *Sumi-e*: Zen black ink wash, dynamic calligraphy brushstrokes, and negative space (*ma*).
     - *90s Retro Cel Anime*: Hand-painted cel animation, film grain, and nostalgic warm lighting.

4. **"Behind the Butai" (裏舞台 - Ura-Butai) Narrator Mode**:
   - Side-by-side trilingual transcripts (Devanagari, English, and Japanese with furigana/romaji).
   - Kamishibai stage notes (*Enshutsu*): pacing cues, card draw speed, vocal inflections, and pauses.
   - Interactive Live Soundboard: Hyoshigi clappers, Taiko drum, and paper slide.
   - Cross-cultural educational commentary bridging Indian philosophical morals (*Mitra-bheda*) with Japanese cultural parallels (*Saru to Wani*).

5. **Wav2Lip Lip-Sync Pipeline**:
   - Script and runner for synchronizing character mouth movements with speech audio for video previews.

---

## 🏗️ Architecture & Project Structure

```
ai-kamishibai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes_narrative.py   # LangChain LLM narrative segmentation
│   │   │   ├── routes_image.py       # SDXL & procedural visual generation
│   │   │   └── routes_audio.py       # Multilingual neural TTS & Wav2Lip
│   │   ├── core/
│   │   │   ├── config.py             # Settings, voice configs, and style definitions
│   │   │   └── prompts.py            # LangChain prompts & Kamishibai templates
│   │   ├── pipeline/
│   │   │   ├── narrative_segmenter.py # LangChain story segmentation & presets
│   │   │   ├── image_generator.py    # Diffusers SDXL + procedural artwork engine
│   │   │   ├── tts_generator.py      # Edge-TTS trilingual voiceover & SFX
│   │   │   └── wav2lip_runner.py     # Wav2Lip character animation pipeline
│   │   └── main.py                   # FastAPI server & asset pre-generation
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── components/
│   │   ├── DigitalButai.jsx          # Wooden stage UI & panel slider
│   │   ├── LanguageSelector.jsx      # EN / HI / JA toggle & neural voice badges
│   │   ├── NarratorPanel.jsx         # Rear view with stage notes & soundboard
│   │   └── StoryForm.jsx             # Story input & 2-way style matrix
│   ├── pages/
│   │   ├── _app.js                   # Application wrapper & global styles
│   │   ├── index.js                  # Landing & Story Library
│   │   └── stage.js                  # Main Kamishibai player stage
│   ├── public/
│   │   ├── audio/                    # Pre-generated neural MP3s & WAV SFX
│   │   └── panels/                   # Pre-generated 4:3 Kamishibai cards
│   ├── styles/
│   │   └── globals.css               # Butai wood textures & slide animations
│   ├── package.json
│   ├── next.config.js
│   └── tailwind.config.js
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js**: v18+ (tested on v22.17)
- **Python**: v3.10+ (tested on v3.13)
- **Optional**: NVIDIA GPU with CUDA for local SDXL inference; OpenAI/Gemini API key for LLM segmentation.

---

### Step 1: Start the Backend (FastAPI)

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend starts at `http://localhost:8000`.  
API documentation is available at `http://localhost:8000/docs`.

---

### Step 2: Start the Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your web browser.

---

## 🎮 Stage Controls & Hotkeys

| Key / Control | Action |
|:---:|:---|
| <kbd>Space</kbd> | Play / Pause Narration Audio |
| <kbd>→</kbd> | Slide Out Card to Next Panel |
| <kbd>←</kbd> | Slide Back to Previous Panel |
| <kbd>U</kbd> / <kbd>N</kbd> | Toggle "Behind the Butai" (裏舞台) Narrator View |
| **Half-Pull (抜き方)** | Tease audience suspense with 45% card pull |
| **開幕 / 閉幕** | Open / Close traditional folding wooden doors (*Tobira*) |

---

## 📡 REST API Reference

### 1. Narrative Segmentation (`/api/narrative`)
- `GET /api/narrative/presets`: Retrieve list of pre-configured Panchatantra & Jataka tales.
- `GET /api/narrative/presets/{story_id}`: Get full panel breakdown for a preset.
- `POST /api/narrative/segment`: Decompose raw story text into sequential panels.
- `GET /api/narrative/styles`: Get available Indian folk, Japanese traditional, and fusion styles.

### 2. Visual Generation (`/api/image`)
- `POST /api/image/generate-panel`: Generate image for a single panel.
- `POST /api/image/batch-generate`: Generate all panel images for a story.
- `GET /api/image/panel/{story_id}/{panel_id}`: Stream JPEG panel card.

### 3. Audio Narration (`/api/audio`)
- `POST /api/audio/synthesize`: Synthesize neural audio for a panel in `en`, `hi`, or `ja`.
- `POST /api/audio/batch-synthesize`: Synthesize all audio tracks across all 3 languages.
- `GET /api/audio/stream/{story_id}/{panel_id}/{lang}`: Stream audio file.
- `GET /api/audio/sound-effect/{sfx_name}`: Stream sound effect (`hyoshigi`, `taiko`, `paper_slide`).
- `POST /api/audio/wav2lip`: Generate Wav2Lip character talking video preview.

---

## 🏛️ Cultural & Historical Background

### The Kamishibai Street-Theater Tradition
During the 1930s to 1950s in Japan, Kamishibai storytellers (*Kamishibaiya-san*) cycled to street corners with a wooden box theater mounted on the back of their bicycles. They clacked **Hyoshigi** wooden clappers to summon neighborhood children, sold traditional barley candies (*Mizuame*), and dramatically slid illustrated paper cards while reading the serialized cliffhanger scripts inscribed on the back of the cards.

### The Indo-Japanese Folklore Bridge
Indian Buddhist fables (*Jatakas*) and wisdom tales (*Panchatantra*) traveled along the maritime and continental Silk Roads into East Asia, becoming deeply rooted in Japanese classical literature (*Konjaku Monogatarishū*) and folkloric archetypes. **AI Kamishibai** revives this historic cross-cultural exchange through modern generative AI, connecting digital-native audiences with ancient world heritage.
