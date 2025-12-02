"""
Verification script to validate JSON output from the autonomous generator.
"""
import json
import sys


def verify_json_structure(data):
    """Validate JSON structure against requirements"""
    errors = []
    
    if not isinstance(data, list):
        errors.append("Output must be a JSON array, not an object or other type")
        return errors
    
    if len(data) == 0:
        errors.append("Output array is empty")
        return errors
    
    print(f"✓ Output is a list with {len(data)} items")
    
    # Count video and image prompts
    video_count = sum(1 for item in data if item.get('type') == 'video')
    image_count = sum(1 for item in data if item.get('type') == 'image')
    
    print(f"✓ Found {video_count} video prompts and {image_count} image prompts")
    
    # Validate each item
    required_video_fields = [
        'id', 'type', 'model', 'topic', 'hook', 'prompt',
        'duration_seconds', 'aspect_ratio', 'style_notes', 'cta_overlay', 'language'
    ]
    
    required_image_fields = required_video_fields.copy()
    
    for i, item in enumerate(data):
        item_type = item.get('type', 'unknown')
        
        # Check required fields
        if item_type == 'video':
            for field in required_video_fields:
                if field not in item:
                    errors.append(f"Item {i} (video): Missing field '{field}'")
            
            # Validate specific fields
            if 'duration_seconds' in item:
                duration = item['duration_seconds']
                if not (5 <= duration <= 30):
                    errors.append(f"Item {i} (video): Duration {duration}s not in 5-30 range")
            
            if item.get('model') != 'video-model':
                errors.append(f"Item {i} (video): Model should be 'video-model', got '{item.get('model')}'")
        
        elif item_type == 'image':
            for field in required_image_fields:
                if field not in item:
                    errors.append(f"Item {i} (image): Missing field '{field}'")
            
            if item.get('model') != 'gpt-image-1-mini':
                errors.append(f"Item {i} (image): Model should be 'gpt-image-1-mini', got '{item.get('model')}'")
            
            if item.get('duration_seconds') != 0:
                errors.append(f"Item {i} (image): Duration should be 0, got {item.get('duration_seconds')}")
        
        else:
            errors.append(f"Item {i}: Invalid type '{item_type}', must be 'video' or 'image'")
        
        # Check aspect ratio
        if item.get('aspect_ratio') != '9:16':
            errors.append(f"Item {i}: Aspect ratio should be '9:16', got '{item.get('aspect_ratio')}'")
        
        # Check language
        if item.get('language') != 'en':
            errors.append(f"Item {i}: Language should be 'en', got '{item.get('language')}'")
    
    return errors


def verify_content_quality(data):
    """Check for content quality indicators"""
    issues = []
    
    video_items = [item for item in data if item.get('type') == 'video']
    
    # Check for emotional angles (look for keywords in prompts)
    emotional_keywords = ['fear', 'greed', 'hope', 'regret', 'relief', 'surprise', 
                          'panic', 'excited', 'nervous', 'confident', 'terrified', 'worried']
    
    items_with_emotion = 0
    for item in video_items:
        prompt_lower = item.get('prompt', '').lower()
        if any(keyword in prompt_lower for keyword in emotional_keywords):
            items_with_emotion += 1
    
    emotion_ratio = items_with_emotion / len(video_items) if video_items else 0
    print(f"✓ {items_with_emotion}/{len(video_items)} video prompts include emotional angles ({emotion_ratio:.0%})")
    
    if emotion_ratio < 0.5:
        issues.append(f"Only {emotion_ratio:.0%} of videos include emotional indicators (should be higher)")
    
    # Check for human-centered content
    human_keywords = ['trader', 'person', 'man', 'woman', 'face', 'eyes', 'hand', 'people', 
                      'family', 'investor', 'character', 'subject']
    
    items_with_humans = 0
    for item in video_items:
        prompt_lower = item.get('prompt', '').lower()
        if any(keyword in prompt_lower for keyword in human_keywords):
            items_with_humans += 1
    
    human_ratio = items_with_humans / len(video_items) if video_items else 0
    print(f"✓ {items_with_humans}/{len(video_items)} video prompts are human-centered ({human_ratio:.0%})")
    
    if human_ratio < 0.6:
        issues.append(f"Only {human_ratio:.0%} of videos are human-centered (should prioritize humans)")
    
    # Check for cinematic descriptions (lighting, camera, mood)
    cinematic_keywords = ['lighting', 'camera', 'shot', 'zoom', 'close-up', 'cinematic', 
                          'shadows', 'dramatic', 'glow', 'mood', 'angle', 'focus']
    
    items_with_cinematic = 0
    for item in video_items:
        prompt_lower = item.get('prompt', '').lower()
        if any(keyword in prompt_lower for keyword in cinematic_keywords):
            items_with_cinematic += 1
    
    cinematic_ratio = items_with_cinematic / len(video_items) if video_items else 0
    print(f"✓ {items_with_cinematic}/{len(video_items)} video prompts have cinematic descriptions ({cinematic_ratio:.0%})")
    
    return issues


if __name__ == "__main__":
    # Load test file
    try:
        with open('output/autonomous_ideas.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ No autonomous_ideas.json file found in output/")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)
    
    print("="*60)
    print("JSON STRUCTURE VALIDATION")
    print("="*60)
    
    structure_errors = verify_json_structure(data)
    
    if structure_errors:
        print("\n❌ Structure validation failed:")
        for error in structure_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ All structure checks passed!")
    
    print("\n" + "="*60)
    print("CONTENT QUALITY VALIDATION")
    print("="*60)
    
    quality_issues = verify_content_quality(data)
    
    if quality_issues:
        print("\n⚠️  Quality concerns:")
        for issue in quality_issues:
            print(f"  - {issue}")
    else:
        print("\n✅ All quality checks passed!")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total prompts: {len(data)}")
    print(f"Videos: {sum(1 for x in data if x.get('type') == 'video')}")
    print(f"Images: {sum(1 for x in data if x.get('type') == 'image')}")
    print(f"Status: {'✅ VALID' if not structure_errors else '❌ FAILED'}")
