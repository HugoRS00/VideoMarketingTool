import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Configuration
VIDEO_MODEL = os.getenv("VIDEO_MODEL", "budget")  # Options: "sora-2", "veo", "budget"
CONTENT_MODE = os.getenv("CONTENT_MODE", "MEME") # Options: "MEME", "INFORMAL", "EDUCATIONAL", "NEWS"

# Autonomous Content Generation Settings
VIDEO_PROMPTS_MIN = int(os.getenv("VIDEO_PROMPTS_MIN", "10"))
VIDEO_PROMPTS_MAX = int(os.getenv("VIDEO_PROMPTS_MAX", "20"))
IMAGE_PROMPTS_MIN = int(os.getenv("IMAGE_PROMPTS_MIN", "5"))
IMAGE_PROMPTS_MAX = int(os.getenv("IMAGE_PROMPTS_MAX", "10"))

# Content mix: 70% serious/educational, 30% meme/absurd
SERIOUS_CONTENT_RATIO = float(os.getenv("SERIOUS_CONTENT_RATIO", "0.70"))
MEME_CONTENT_RATIO = float(os.getenv("MEME_CONTENT_RATIO", "0.30"))

# Target Audience
TARGET_AUDIENCES = [
    "retail traders",
    "crypto bros", 
    "finance TikTok",
    "meme traders",
    "beginners",
    "intermediates"
]

# Emotional Angles
EMOTIONAL_ANGLES = ["greed", "fear", "hope", "regret", "relief", "surprise"]

# Paths
FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Ensure directories exist
os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
