import random
from trends import TrendSpotter
from prompt_factory import PromptFactory
from schemas import VideoPrompt, ImagePrompt
from config import (
    VIDEO_PROMPTS_MIN, VIDEO_PROMPTS_MAX,
    IMAGE_PROMPTS_MIN, IMAGE_PROMPTS_MAX,
    SERIOUS_CONTENT_RATIO, MEME_CONTENT_RATIO
)


class FinanceIdeaGenerator:
    """
    Autonomous finance TikTok content generator.
    
    On every run, with no user input:
    1. Searches web for latest finance news, market events, viral memes
    2. Picks 5-15 high potential topics
    3. Generates cinematic video and image prompts
    4. Returns pure JSON array
    """
    
    def __init__(self):
        self.trend_spotter = TrendSpotter()
        self.prompt_factory = PromptFactory()
        
    def generate_ideas(self) -> list[dict]:
        """
        Main autonomous generation method.
        Returns list of video and image prompt dictionaries.
        """
        print("🎬 Starting autonomous finance content generation...")
        
        # Step 1: Get trending topics (5-15 topics)
        print("📊 Fetching trending finance topics...")
        topics = self.trend_spotter.get_high_potential_topics(count_range=(5, 15))
        print(f"✓ Found {len(topics)} high-potential topics")
        
        # Step 2: Determine video and image counts
        video_count = random.randint(VIDEO_PROMPTS_MIN, VIDEO_PROMPTS_MAX)
        image_count = random.randint(IMAGE_PROMPTS_MIN, IMAGE_PROMPTS_MAX)
        print(f"🎥 Generating {video_count} video prompts and {image_count} image prompts...")
        
        all_prompts = []
        
        # Step 3: Generate video prompts
        print("\n🎬 Creating video prompts...")
        video_topics = self._select_topics_for_videos(topics, video_count)
        
        for i, topic_data in enumerate(video_topics, 1):
            topic = topic_data['topic']
            is_meme = topic_data['category'] in ['meme', 'story']
            
            print(f"  [{i}/{video_count}] {topic} {'(MEME)' if is_meme else '(SERIOUS)'}")
            video_prompt = self.prompt_factory.create_video_prompt(topic, is_meme=is_meme)
            all_prompts.append(video_prompt.model_dump())
        
        # Step 4: Generate image prompts (typically more meme-focused)
        print("\n🖼️  Creating image prompts...")
        image_topics = self._select_topics_for_images(topics, image_count)
        
        for i, topic_data in enumerate(image_topics, 1):
            topic = topic_data['topic']
            is_meme = True  # Images are typically meme-friendly
            
            print(f"  [{i}/{image_count}] {topic}")
            image_prompt = self.prompt_factory.create_image_prompt(topic, is_meme=is_meme)
            all_prompts.append(image_prompt.model_dump())
        
        # Step 5: Shuffle for variety
        random.shuffle(all_prompts)
        
        print(f"\n✨ Successfully generated {len(all_prompts)} total prompts!")
        print(f"   • {video_count} video prompts")
        print(f"   • {image_count} image prompts")
        
        return all_prompts
    
    def _select_topics_for_videos(self, topics: list[dict], count: int) -> list[dict]:
        """
        Select topics for video generation ensuring proper serious/meme ratio.
        """
        # Calculate how many should be serious vs meme
        meme_count = int(count * MEME_CONTENT_RATIO)
        serious_count = count - meme_count
        
        # Separate topics by type
        meme_topics = [t for t in topics if t['category'] in ['meme', 'story']]
        serious_topics = [t for t in topics if t['category'] not in ['meme', 'story']]
        
        selected = []
        
        # Add meme topics
        if len(meme_topics) >= meme_count:
            selected.extend(random.sample(meme_topics, meme_count))
        else:
            selected.extend(meme_topics)
            # Fill remaining with serious topics converted to meme style
            remaining = meme_count - len(meme_topics)
            if serious_topics and remaining > 0:
                for topic in random.sample(serious_topics, min(remaining, len(serious_topics))):
                    meme_version = topic.copy()
                    meme_version['category'] = 'meme'
                    selected.append(meme_version)
        
        # Add serious topics
        if len(serious_topics) >= serious_count:
            selected.extend(random.sample(serious_topics, serious_count))
        else:
            selected.extend(serious_topics)
            # Fill remaining with meme topics converted to serious style
            remaining = serious_count - len(serious_topics)
            if meme_topics and remaining > 0:
                for topic in random.sample(meme_topics, min(remaining, len(meme_topics))):
                    serious_version = topic.copy()
                    serious_version['category'] = 'education'
                    selected.append(serious_version)
        
        return selected[:count]
    
    def _select_topics_for_images(self, topics: list[dict], count: int) -> list[dict]:
        """
        Select topics for image generation (typically favors meme content).
        """
        # Images work better as memes, so prioritize those
        meme_topics = [t for t in topics if t['category'] in ['meme', 'story']]
        other_topics = [t for t in topics if t['category'] not in ['meme', 'story']]
        
        selected = []
        
        # Try to get mostly meme topics
        if len(meme_topics) >= count:
            selected = random.sample(meme_topics, count)
        else:
            selected.extend(meme_topics)
            remaining = count - len(meme_topics)
            if other_topics and remaining > 0:
                # Convert serious topics to meme-style images
                for topic in random.sample(other_topics, min(remaining, len(other_topics))):
                    meme_version = topic.copy()
                    meme_version['topic'] = f"POV: {topic['topic']}"  # Make it meme-friendly
                    selected.append(meme_version)
        
        return selected[:count]


if __name__ == "__main__":
    # Test the autonomous generator
    import json
    
    generator = FinanceIdeaGenerator()
    ideas = generator.generate_ideas()
    
    # Output pure JSON (as required)
    print("\n" + "="*60)
    print("FINAL JSON OUTPUT:")
    print("="*60)
    print(json.dumps(ideas, indent=2))
    
    # Save to file for testing
    with open('output/autonomous_ideas.json', 'w') as f:
        json.dump(ideas, f, indent=2)
    
    print(f"\n✓ Saved to output/autonomous_ideas.json")
