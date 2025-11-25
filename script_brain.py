import json
import os
from openai import OpenAI
from config import OPENAI_API_KEY


class ScriptBrain:
    def __init__(self):
        self.model = "gpt-4o" # Using gpt-4o as proxy for gpt-5.1 for now
        if OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        else:
            self.client = None


    def _get_system_prompt(self, mode):
        base_prompt = (
            "You are 'Kai', the TradingWizard AI. You are a cynical, smart, fast-paced, slightly rogue AI. "
            "Your goal is to create viral short-form video scripts (TikTok/Reels) for Gen Z/Millennial traders. "
            "CRITICAL RULE: NO PREAMBLE. No 'Welcome back'. No 'Listen up'. No 'Just in'. "
            "Start immediately with the subject, the number, or the punchline. "
            "Provide the output in JSON format with keys: 'script' (the spoken text), 'visual_prompts' (list of strings describing visuals for each scene)."
        )

        if mode == "MEME":
            return base_prompt + (
                " MODE: MEME (The Shitposter). "
                "Goal: Pure entertainment/virality. "
                "Tone: Absurdist, heavy slang (fr, ong, cap), mocking losses. "
                "Structure: Quick setup -> Punchline -> Visual chaos. "
                "Visuals: Distorted imagery, rapid loops, 'deep fried' aesthetics."
            )
        elif mode == "INFORMAL":
            return base_prompt + (
                " MODE: INFORMAL (The Vibe Check). "
                "Goal: Relatability and parasocial connection. "
                "Tone: Casual, vlogging style, 'just woke up' energy. "
                "Structure: 'I just saw this chart...' -> 'It looks like...' -> 'Here is what I'm doing.' "
                "Visuals: POV shots of screens, coffee, late-night coding setups."
            )
        elif mode == "EDUCATIONAL":
            return base_prompt + (
                " MODE: EDUCATIONAL (The Alpha). "
                "Goal: High value, saveable content. "
                "Tone: Authoritative but fast. No fluff. "
                "Structure: Hook ('Stop using RSI like this') -> The Mistake -> The Fix -> TradingWizard Flex. "
                "Visuals: Clean data visualizations, glowing charts, step-by-step overlays."
            )
        elif mode == "NEWS":
            return base_prompt + (
                " MODE: NEWS (The Terminal). "
                "Goal: Breaking updates with a cynical twist. "
                "Tone: Deadpan, fast, factual but rude. Start directly with the noun. "
                "Example Start: 'Nvidia earnings just missed. The AI bubble isn't popping, but your calls are dead.' "
                "Structure: [The Data Point/Event] -> [Why it matters] -> [Who is getting wrecked]. "
                "Visuals: Spinning globes, ticker tapes, matrix-style data streams."
            )
        else:
            return base_prompt

    def generate_script(self, topic, mode="MEME"):
        if not self.client:
            print("Error: OPENAI_API_KEY not set.")
            return None

        system_prompt = self._get_system_prompt(mode)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a viral video script about: {topic}"}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error generating script: {e}")
            return None

if __name__ == "__main__":
    brain = ScriptBrain()
    # Test MEME mode
    print("MEME Script:", brain.generate_script("Bitcoin crash", "MEME"))
    # Test NEWS mode
    print("NEWS Script:", brain.generate_script("Nvidia earnings", "NEWS"))
