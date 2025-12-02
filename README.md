# Finance TikTok Autonomous Content Generator 🎬

An autonomous AI-powered idea generator for finance TikTok content. Searches the web for the latest finance news, market events, and viral memes, then generates cinematic video and image prompts for AI models.

## 🚀 Quick Start

### Run Autonomous Generator (Standalone)
```bash
python3 idea_generator.py
```

Outputs pure JSON array and saves to `output/autonomous_ideas.json`

### Run as API Server
```bash
python3 main.py
```

Then call the endpoint:
```bash
curl http://localhost:8000/generate
```

Returns pure JSON array with 10-20 video prompts and 5-10 image prompts.

## 📋 Output Format

Each prompt object contains:
```json
{
  "id": "short-identifier",
  "type": "video" | "image",
  "model": "video-model" | "gpt-image-1-mini",
  "topic": "description of finance topic",
  "hook": "punchy 1-sentence hook for viewers",
  "prompt": "full cinematic production prompt",
  "duration_seconds": 5-30,  // 0 for images
  "aspect_ratio": "9:16",
  "style_notes": "style hints",
  "cta_overlay": "call-to-action text",
  "language": "en"
}
```

## 🎯 Features

- **Fully Autonomous** - No user input required
- **Web Search** - Google Trends + finance news + social memes
- **Smart Selection** - 5-15 high-potential topics per run
- **Content Mix** - 70% serious/educational, 30% meme/absurd
- **Emotional Angles** - Every prompt includes greed, fear, hope, regret, relief, or surprise
- **Human-Centered** - Prioritizes people over charts
- **Cinematic** - Detailed lighting, camera, and mood descriptions
- **9:16 Vertical** - Optimized for TikTok/Reels

## 🎨 Target Audience

- Retail traders
- Crypto bros
- Finance TikTok creators
- Meme traders
- Beginners and intermediates

## 🧪 Validation

Run validation script to check output quality:
```bash
python3 verify_schemas.py
```

Checks:
- ✅ JSON structure compliance
- ✅ Required fields present
- ✅ Emotional angle coverage
- ✅ Human-centered descriptions
- ✅ Cinematic details

## 📁 Project Structure

```
VideoMarketingTool/
├── idea_generator.py      # Main autonomous orchestrator
├── prompt_factory.py      # Cinematic prompt generator (OpenAI)
├── trends.py              # Enhanced trend detection
├── schemas.py             # Pydantic validation models
├── config.py              # Configuration settings
├── main.py                # FastAPI server with /generate endpoint
├── verify_schemas.py      # Output validation script
└── output/
    └── autonomous_ideas.json  # Generated prompts
```

## ⚙️ Configuration

Edit `config.py` or set environment variables:

```python
VIDEO_PROMPTS_MIN = 10
VIDEO_PROMPTS_MAX = 20
IMAGE_PROMPTS_MIN = 5
IMAGE_PROMPTS_MAX = 10
SERIOUS_CONTENT_RATIO = 0.70
MEME_CONTENT_RATIO = 0.30
```

## 🔑 API Keys Required

Set in `.env` file:
```bash
OPENAI_API_KEY=your_key_here
REPLICATE_API_TOKEN=your_key_here  # Optional, for video generation
GOOGLE_API_KEY=your_key_here       # Optional, for Veo 2
ELEVENLABS_KEY=your_key_here       # Optional, for audio
```

## 📊 Example Output

**Video Prompt:**
```json
{
  "id": "lone-day-trader-thriller",
  "type": "video",
  "model": "video-model",
  "topic": "retail trader taking one last high risk trade",
  "hook": "She has one trade left to fix her whole year.",
  "prompt": "A cinematic shot of a lone day trader, ANNA, 35, tired eyes and messy bun, in a dark high rise apartment at night. Multiple screens glow with chaotic stock charts as city lights twinkle outside...",
  "duration_seconds": 12,
  "aspect_ratio": "9:16",
  "style_notes": "thriller, handheld micro jitters, dramatic lighting",
  "cta_overlay": "Would you take this trade?",
  "language": "en"
}
```

**Image Prompt:**
```json
{
  "id": "fridge-monster-inflation",
  "type": "image",
  "model": "gpt-image-1-mini",
  "topic": "inflation making groceries terrifying",
  "hook": "POV: you check food prices in 2025.",
  "prompt": "A comedic horror image where a huge fuzzy money eating monster climbs out of an open fridge in a small apartment kitchen...",
  "duration_seconds": 0,
  "aspect_ratio": "9:16",
  "style_notes": "meme friendly, exaggerated expressions",
  "cta_overlay": "",
  "language": "en"
}
```

## 🎥 Content Quality

All prompts include:
- ✅ Emotional angle (greed/fear/hope/regret/relief/surprise)
- ✅ Human subjects with facial expressions
- ✅ Cinematic details (lighting, camera angles, mood)
- ✅ Punchy hooks suitable for voiceover
- ✅ No watermarks, logos, or baked-in text
- ✅ 5-30 second duration for videos
- ✅ 9:16 vertical aspect ratio

## 📞 API Endpoints

- `GET /generate` - Generate autonomous content ideas (pure JSON array)
- `GET /health` - Health check
- `GET /trends` - View trending topics
- `GET /` - Web UI (interactive mode)

## 🧑‍💻 Development

**Test the generator:**
```bash
python3 idea_generator.py
```

**Validate output:**
```bash
python3 verify_schemas.py
```

**Start API server:**
```bash
python3 main.py
```

**Test API:**
```bash
curl http://localhost:8000/generate | python3 -m json.tool
```

## 📝 License

Private project for TradingWizard AI content generation.
