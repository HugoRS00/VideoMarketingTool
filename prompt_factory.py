import random
import json
from openai import OpenAI
from config import OPENAI_API_KEY
from schemas import VideoPrompt, ImagePrompt


class PromptFactory:
    """Generates cinematic video and image prompts for finance TikTok content"""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.emotional_angles = ["greed", "fear", "hope", "regret", "relief", "surprise"]
        self.video_styles = [
            "thriller, handheld micro jitters, dramatic lighting",
            "family friendly, slapstick, oversaturated",
            "low contrast, VHS grain, intimate",
            "cinematic, subtle camera motion, grounded realism",
            "horror comedy, high contrast, exaggerated expressions",
            "documentary style, warm tones, natural light",
            "cyberpunk, neon lights, dark mood",
            "pixar style, 3D animation, vibrant colors"
        ]
        
    def _get_system_prompt(self, content_type: str, is_meme: bool):
        """Generate system prompt for OpenAI based on content type"""
        base_rules = """You are a viral finance content creator for TikTok/Reels.
Target audience: retail traders, crypto bros, finance TikTok, meme traders, beginners and intermediates.

CRITICAL RULES:
- Focus ONLY on finance, markets, money, risk, wealth, trading psychology, and memes around these
- Hooks must be punchy and curiosity driven, suitable for subtitles and voiceover
- Visuals must be simple enough for 5-30 second TikToks but vivid and cinematic
- ALWAYS include emotional angle: greed, fear, hope, regret, relief, or surprise
- Prefer human-centered shots over generic candlestick charts
- Never include watermarks, logos, app UI, or text baked into the image/video (only describe visuals)
- Be specific about lighting, camera movement, mood, and visual details
- Output ONLY valid JSON matching the exact schema provided"""

        if content_type == "video":
            specific = """
VIDEO REQUIREMENTS:
- Duration: 5-30 seconds
- Aspect ratio: 9:16 (vertical)
- Include cinematic camera angles, lighting descriptions, and mood
- Describe human subjects with emotional expressions and body language
- Include sound design notes when relevant (ambient sounds, music hints)
- Style can range from thriller to comedy to documentary"""
        else:  # image
            specific = """
IMAGE REQUIREMENTS:
- Single frame, high impact
- Aspect ratio: 9:16 (vertical)
- Colorful, high contrast, cinematic lighting
- Suitable for thumbnail or standalone meme
- Can be realistic, 3D rendered, or illustrated
- Must stop scroll - visually arresting"""
        
        tone = "absurd, meme-friendly, exaggerated, comedic" if is_meme else "educational, serious, authoritative, fast-paced"
        
        return f"{base_rules}\n{specific}\n\nTONE for this prompt: {tone}"
    
    def create_video_prompt(self, topic: str, is_meme: bool = False) -> VideoPrompt:
        """Generate a single video prompt using OpenAI"""
        if not self.client:
            return self._create_fallback_video(topic, is_meme)
        
        emotional_angle = random.choice(self.emotional_angles)
        duration = random.randint(5, 30)
        style_notes = random.choice(self.video_styles)
        
        system_prompt = self._get_system_prompt("video", is_meme)
        user_prompt = f"""Generate a viral TikTok video prompt about: {topic}

Requirements:
- Emotional angle: {emotional_angle}
- Duration: {duration} seconds
- Style: {style_notes}
- Human-centered (show people, faces, emotions)
- Cinematic and detailed

Return JSON with these exact keys:
{{
  "id": "short-kebab-case-id",
  "hook": "one sentence hook for viewers",
  "prompt": "detailed cinematic production prompt",
  "cta_overlay": "optional call-to-action text or empty string"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                timeout=30.0
            )
            
            data = json.loads(response.choices[0].message.content)
            
            return VideoPrompt(
                id=data.get("id", self._generate_id(topic)),
                type="video",
                model="video-model",
                topic=topic,
                hook=data["hook"],
                prompt=data["prompt"],
                duration_seconds=duration,
                aspect_ratio="9:16",
                style_notes=style_notes,
                cta_overlay=data.get("cta_overlay", ""),
                language="en"
            )
            
        except Exception as e:
            print(f"Error generating video prompt: {e}")
            return self._create_fallback_video(topic, is_meme)
    
    def create_image_prompt(self, topic: str, is_meme: bool = True) -> ImagePrompt:
        """Generate a single image prompt using OpenAI"""
        if not self.client:
            return self._create_fallback_image(topic, is_meme)
        
        emotional_angle = random.choice(self.emotional_angles)
        
        system_prompt = self._get_system_prompt("image", is_meme)
        user_prompt = f"""Generate a viral TikTok image/thumbnail prompt about: {topic}

Requirements:
- Emotional angle: {emotional_angle}
- Meme-friendly and scroll-stopping
- High contrast, colorful, cinematic
- Human-centered or character-focused

Return JSON with these exact keys:
{{
  "id": "short-kebab-case-id",
  "hook": "one sentence hook for viewers",
  "prompt": "detailed image generation prompt",
  "style_notes": "brief style description",
  "cta_overlay": "optional call-to-action text or empty string"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                timeout=30.0
            )
            
            data = json.loads(response.choices[0].message.content)
            
            return ImagePrompt(
                id=data.get("id", self._generate_id(topic)),
                type="image",
                model="gpt-image-1-mini",
                topic=topic,
                hook=data["hook"],
                prompt=data["prompt"],
                duration_seconds=0,
                aspect_ratio="9:16",
                style_notes=data.get("style_notes", "meme friendly, high contrast"),
                cta_overlay=data.get("cta_overlay", ""),
                language="en"
            )
            
        except Exception as e:
            print(f"Error generating image prompt: {e}")
            return self._create_fallback_image(topic, is_meme)

    def create_kai_prompt(self, topic: str) -> VideoPrompt:
        """Generate a 'Kai Zen' character video prompt"""
        if not self.client:
            return self._create_fallback_video(topic, is_meme=True)
            
        system_prompt = """You are the creator of 'Kai', the TradingWizard mascot.
CHARACTER: Kai is a tiny wizard with a floppy hat. He is calm, zen, and magical.
ACTIVITY: He is often stacking pebbles, meditating, or interacting with trading charts in a peaceful, lofi way.
VIBE: Lofi beats, slow motion, magical realism, cute but profound, zero emotion/stoic.

EXAMPLES:
- tiny kai in floppy wizard hat sits by a lake, calmly stacking pebbles into a perfect cairn while the chart behind him prints a 20r green candle in slow motion, soft lofi beats
- kai levitates a single pebble above his hand, eyes wide, then gently places it on a rock stack as the bitcoin chart hits exact tp, peaceful wind chimes sfx
- kai blinks slowly at a red candle, tilts his hat, floats one pebble higher, candle instantly flips green, zero emotion
- kai asleep on a lily pad, hat covering eyes, pebbles auto-stacking themselves around him while +47% pnl floats overhead like fireflies

GOAL: Create a similar video prompt involving Kai and the given finance topic."""

        user_prompt = f"""Generate a Kai Zen video prompt about: {topic}

Return JSON with these exact keys:
{{
  "id": "kai-zen-id",
  "hook": "short zen/lofi hook",
  "prompt": "full prompt describing tiny kai with floppy hat and pebbles",
  "cta_overlay": "minimal text or empty"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                timeout=30.0
            )
            
            data = json.loads(response.choices[0].message.content)
            
            return VideoPrompt(
                id=data.get("id", f"kai-{self._generate_id(topic)}"),
                type="video",
                model="video-model",
                topic=topic,
                hook=data["hook"],
                prompt=data["prompt"],
                duration_seconds=random.randint(8, 15),
                aspect_ratio="9:16",
                style_notes="lofi, zen, magical realism, 3d render, cute",
                cta_overlay=data.get("cta_overlay", ""),
                language="en"
            )
            
        except Exception as e:
            print(f"Error generating Kai prompt: {e}")
            return self._create_fallback_video(topic, is_meme=True)

    
    def _generate_id(self, topic: str) -> str:
        """Generate a kebab-case ID from topic"""
        import re
        clean = re.sub(r'[^a-z0-9\s-]', '', topic.lower())
        return '-'.join(clean.split()[:4])
    
    def _create_fallback_video(self, topic: str, is_meme: bool) -> VideoPrompt:
        """Create a basic fallback video prompt if API fails"""
        return VideoPrompt(
            id=self._generate_id(topic),
            type="video",
            model="video-model",
            topic=topic,
            hook=f"This changes everything about {topic}.",
            prompt=f"A cinematic shot of a trader reacting to {topic}. Dark room, multiple glowing screens, dramatic lighting. 9:16 vertical format.",
            duration_seconds=10,
            aspect_ratio="9:16",
            style_notes="cinematic, dramatic lighting",
            cta_overlay="What would you do?",
            language="en"
        )
    
    def _create_fallback_image(self, topic: str, is_meme: bool) -> ImagePrompt:
        """Create a basic fallback image prompt if API fails"""
        return ImagePrompt(
            id=self._generate_id(topic),
            type="image",
            model="gpt-image-1-mini",
            topic=topic,
            hook=f"POV: when {topic} happens.",
            prompt=f"A comedic meme-style image showing an exaggerated reaction to {topic}. Colorful, high contrast, 9:16 vertical.",
            duration_seconds=0,
            aspect_ratio="9:16",
            style_notes="meme friendly, exaggerated",
            cta_overlay="",
            language="en"
        )


if __name__ == "__main__":
    # Test the factory
    factory = PromptFactory()
    
    print("Testing video prompt generation...")
    video = factory.create_video_prompt("Bitcoin crashes 20% in one day", is_meme=False)
    print(json.dumps(video.model_dump(), indent=2))
    
    print("\nTesting image prompt generation...")
    image = factory.create_image_prompt("Checking your portfolio during a bull run", is_meme=True)
    print(json.dumps(image.model_dump(), indent=2))
