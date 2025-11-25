import os
import sys
from script_brain import ScriptBrain
from video_factory import VideoProvider
from editor import VideoEditor
from trends import TrendSpotter

def test_trends():
    print("\n--- Testing Trend Spotter ---")
    spotter = TrendSpotter()
    trends = spotter.fetch_trending_topics()
    print(f"Trends: {trends}")
    assert len(trends) > 0, "No trends fetched"

def test_script_brain():
    print("\n--- Testing Script Brain ---")
    brain = ScriptBrain()
    # Test MEME mode
    print("Generating MEME script...")
    meme_script = brain.generate_script("Bitcoin Crash", "MEME")
    if meme_script:
        print(f"MEME Script: {meme_script.get('script')}")
        assert "script" in meme_script
        assert "visual_prompts" in meme_script
    else:
        print("Skipping Script Brain test (likely no API key)")

    # Test NEWS mode (Check for preamble)
    print("Generating NEWS script...")
    news_script = brain.generate_script("Nvidia Earnings", "NEWS")
    if news_script:
        print(f"NEWS Script: {news_script.get('script')}")
        # Basic check for preamble - this is hard to strictly assert without LLM but we can check length or keywords
        assert len(news_script.get('script')) > 0

def test_video_provider():
    print("\n--- Testing Video Provider ---")
    provider = VideoProvider()
    url = provider.generate_video("Test prompt", "budget")
    print(f"Budget Video URL: {url}")
    assert "replicate" in url or "mock" in url

    url_sora = provider.generate_video("Test prompt", "sora-2")
    print(f"Sora Video URL: {url_sora}")
    assert "sora" in url_sora

def test_editor_mock():
    print("\n--- Testing Editor (Mock) ---")
    editor = VideoEditor()
    print(f"Font Path: {editor.font_path}")
    assert editor.font_path is not None

    # Test Multi-Scene Assembly Logic (Mocking files)
    # Ensure dummy files exist
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Create dummy video files if they don't exist
    dummy_video = "output/temp_background.mp4"
    if not os.path.exists(dummy_video):
        # Create a simple color clip if moviepy is working, else just touch
        # For verification speed, we'll just check if the function accepts the list
        with open(dummy_video, "w") as f:
            f.write("dummy content") 
    
    dummy_audio = "output/mock_audio.mp3"
    if not os.path.exists(dummy_audio):
        with open(dummy_audio, "w") as f:
            f.write("dummy content")

    # We can't run full assemble_video without real media files (MoviePy will fail on text files)
    # So we will just verify the method signature and existence
    assert hasattr(editor, 'assemble_video')
    assert hasattr(editor, 'generate_captions')
    print("Editor methods verified.")

    # Test Caption Generation (Mock call)
    # We can't easily mock the OpenAI client call inside the class without dependency injection or patching
    # But we can check if it handles missing key gracefully
    captions = editor.generate_captions(dummy_audio)
    print(f"Captions (Expect empty or mock): {captions}")
    assert isinstance(captions, list)

if __name__ == "__main__":
    try:
        test_trends()
        test_video_provider()
        test_editor_mock()
        # Script Brain requires API Key, so it might fail in some envs if not set
        if os.getenv("OPENAI_API_KEY"):
            test_script_brain()
        else:
            print("\nSkipping Script Brain test: OPENAI_API_KEY not set")
            
        print("\nALL TESTS PASSED (Mock/Integration)")
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
