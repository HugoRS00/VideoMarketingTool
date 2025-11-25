import os
import sys
from dotenv import load_dotenv

print("--- Verifying Setup ---")

# 1. Check .env loading
load_dotenv()
google_key = os.getenv("GOOGLE_API_KEY")
if google_key:
    print(f"✅ GOOGLE_API_KEY found: {google_key[:5]}...{google_key[-4:]}")
else:
    print("❌ GOOGLE_API_KEY not found in environment")

# 2. Check Google Generative AI import
try:
    import google.generativeai as genai
    print("✅ google.generativeai imported successfully")
    
    if google_key:
        genai.configure(api_key=google_key)
        print("✅ google.generativeai configured with key")
    
except ImportError:
    print("❌ Failed to import google.generativeai")
except Exception as e:
    print(f"❌ Error configuring google.generativeai: {e}")

# 3. Check VideoFactory integration
try:
    from video_factory import VideoProvider
    provider = VideoProvider()
    if provider.has_google:
        print("✅ VideoProvider initialized with Google support")
    else:
        print("⚠️ VideoProvider initialized WITHOUT Google support (check key/dependency)")
except Exception as e:
    print(f"❌ Error initializing VideoProvider: {e}")

print("--- Verification Complete ---")
