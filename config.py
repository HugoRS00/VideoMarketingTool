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

# Paths
FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Ensure directories exist
os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
