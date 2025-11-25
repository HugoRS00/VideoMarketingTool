import os
from dotenv import load_dotenv

load_dotenv()

def check_key(name, start_pattern=None):
    val = os.getenv(name)
    if not val:
        print(f"❌ {name}: Not found")
        return
    
    masked = val[:8] + "..." + val[-4:] if len(val) > 12 else "****"
    print(f"✅ {name}: Found ({masked})")
    
    if start_pattern and not val.startswith(start_pattern):
        print(f"   ⚠️ Warning: {name} usually starts with '{start_pattern}'")

print("--- Checking API Keys ---")
check_key("OPENAI_API_KEY", "sk-")
check_key("ELEVENLABS_KEY") # No strict prefix, usually hex
check_key("GOOGLE_API_KEY", "AIza")
check_key("REPLICATE_API_TOKEN", "r8_")
print("-------------------------")
