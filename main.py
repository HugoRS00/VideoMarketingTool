from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from script_brain import ScriptBrain
from video_factory import VideoProvider
from editor import VideoEditor
import os

app = FastAPI(title="TradingWizard AI - Viral Video Engine")

# Initialize Components
brain = ScriptBrain()
vision = VideoProvider()
editor = VideoEditor()

class VideoRequest(BaseModel):
    topic: str
    model_tier: str = "budget" # "budget", "sora-2", "veo"
    content_mode: str = "MEME" # "MEME", "INFORMAL", "EDUCATIONAL", "NEWS"

@app.post("/generate_video")
async def generate_video_endpoint(request: VideoRequest):
    try:
        # 1. Generate Script
        print(f"Step 1: Generating Script for '{request.topic}' in mode '{request.content_mode}'")
        script_data = brain.generate_script(request.topic, request.content_mode)
        if not script_data:
            raise HTTPException(status_code=500, detail="Failed to generate script")
        
        script_text = script_data.get("script", "")
        visual_prompts = script_data.get("visual_prompts", [])
        
        if not script_text:
             raise HTTPException(status_code=500, detail="Empty script generated")

        # 2. Generate Video (Multi-Scene)
        print(f"Step 2: Generating Videos for {len(visual_prompts)} scenes")
        video_paths = []
        
        # Limit to 3 scenes to save time/cost for now
        scenes_to_generate = visual_prompts[:3] if visual_prompts else [f"Abstract background for {request.topic}"]
        
        for i, prompt in enumerate(scenes_to_generate):
            print(f"  - Generating Scene {i+1}: {prompt}")
            video_url = vision.generate_video(prompt, request.model_tier)
            
            # Download video
            if video_url.startswith("http"):
                try:
                    import requests
                    response = requests.get(video_url)
                    if response.status_code == 200:
                        scene_path = os.path.join("output", f"scene_{i}_{request.topic.replace(' ', '_')}.mp4")
                        with open(scene_path, "wb") as f:
                            f.write(response.content)
                        video_paths.append(scene_path)
                    else:
                        print(f"Failed to download video from {video_url}")
                except Exception as e:
                    print(f"Error downloading video: {e}")
            else:
                # Assume local path or mock
                video_paths.append(video_url)

        if not video_paths:
             # Fallback to dummy if everything failed
             print("Warning: No videos generated. Using fallback.")
             video_paths.append("output/temp_background.mp4")

        # 3. Generate Audio
        print("Step 3: Generating Audio")
        audio_path = editor.generate_audio(script_text)
        
        # 4. Assemble
        print("Step 4: Assembling Final Asset")
        
        # We need at least one valid video file
        valid_videos = [p for p in video_paths if os.path.exists(p)]
        
        if valid_videos:
             final_output = editor.assemble_video(valid_videos, audio_path, script_text, f"viral_{request.content_mode}_{request.topic.replace(' ', '_')}.mp4")
             return {"status": "success", "video_path": final_output, "script": script_text}
        else:
             return {"status": "partial_success", "message": "Video generation failed (no local files), but script and audio created.", "script": script_text, "audio_path": audio_path, "video_urls": [video_url]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from trends import TrendSpotter

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")

# Initialize Trend Spotter
spotter = TrendSpotter()

@app.get("/trends")
def get_trends():
    return spotter.fetch_trending_topics()

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return {"status": "healthy", "persona": "Kai"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
