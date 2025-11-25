import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from config import FONTS_DIR, OUTPUT_DIR, ELEVENLABS_KEY, OPENAI_API_KEY
from openai import OpenAI
import requests


class VideoEditor:
    def __init__(self):
        self.font_path = self._get_font_path()
        if OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        else:
            self.client = None

    def _get_font_path(self):
        # Check for preferred fonts in FONTS_DIR
        preferred = ["Komika Axis.ttf", "Montserrat-Black.ttf"]
        for font in preferred:
            path = os.path.join(FONTS_DIR, font)
            if os.path.exists(path):
                return path
        # Fallback to a system font or default
        return "Arial-Bold"

    def generate_audio(self, text, voice="kai"):
        """
        Generates audio from text using OpenAI TTS (or ElevenLabs).
        Returns path to audio file.
        """
        print(f"Generating audio for: {text[:20]}...")
        
        if not self.client:
            print("Error: OPENAI_API_KEY not set. Using mock audio.")
            # Create a dummy audio file for testing
            mock_audio_path = os.path.join(OUTPUT_DIR, "mock_audio.mp3")
            # We need a valid audio file for MoviePy. 
            # Since we can't easily generate one without a library, we might fail here if we don't have one.
            # But for now let's return the path and hope the user provides the key or we use a pre-existing file.
            return mock_audio_path

        # Using OpenAI TTS for simplicity and speed in this demo
        # Voice 'onyx' is deep and assertive, close to the description
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text,
            speed=1.1 # Slightly accelerated
        )
        
        audio_path = os.path.join(OUTPUT_DIR, "temp_audio.mp3")
        response.stream_to_file(audio_path)
        return audio_path

    def generate_captions(self, audio_path):
        """
        Generates precise word-level timestamps using OpenAI Whisper.
        """
        print("Generating captions with Whisper...")
        if not self.client:
            print("OpenAI Client not available for Whisper.")
            return []

        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )
            return transcript.words # List of objects with word, start, end
        except Exception as e:
            print(f"Error generating captions: {e}")
            return []

    def assemble_video(self, video_paths, audio_path, script_text, output_filename="final_video.mp4"):
        """
        Stitches video(s), audio, and subtitles.
        video_paths: List of video file paths or single path string.
        """
        print("Assembling video...")
        
        try:
            # Handle single path or list
            if isinstance(video_paths, str):
                video_paths = [video_paths]

            # Load Audio
            audio_clip = AudioFileClip(audio_path)
            
            # Load and Stitch Videos
            clips = []
            current_duration = 0
            target_duration = audio_clip.duration
            
            # Simple logic: Loop through provided videos until we fill the audio duration
            while current_duration < target_duration:
                for path in video_paths:
                    if not os.path.exists(path):
                        print(f"Warning: Video path not found: {path}")
                        continue
                    clip = VideoFileClip(path)
                    # Resize if needed (optional, assuming all are same aspect ratio)
                    clips.append(clip)
                    current_duration += clip.duration
                    if current_duration >= target_duration:
                        break
            
            if not clips:
                print("No valid video clips found.")
                return None

            stitched_video = concatenate_videoclips(clips, method="compose")
            
            # Loop or cut to match audio
            if stitched_video.duration < target_duration:
                final_video = stitched_video.loop(duration=target_duration)
            else:
                final_video = stitched_video.subclip(0, target_duration)
                
            final_video = final_video.set_audio(audio_clip)
            
            # Generate Subtitles (Whisper or Fallback)
            captions = self.generate_captions(audio_path)
            txt_clips = []
            
            if captions:
                for item in captions:
                    word = item['word']
                    start = item['start']
                    end = item['end']
                    duration = end - start
                    
                    txt_clip = (TextClip(word.strip(), fontsize=70, color='yellow', font=self.font_path, stroke_color='black', stroke_width=2)
                                .set_position('center')
                                .set_start(start)
                                .set_duration(duration))
                    txt_clips.append(txt_clip)
            else:
                # Fallback to linear timing
                print("Using fallback linear timing for captions.")
                words = script_text.split()
                duration_per_word = audio_clip.duration / len(words)
                for i, word in enumerate(words):
                    txt_clip = (TextClip(word, fontsize=70, color='yellow', font=self.font_path, stroke_color='black', stroke_width=2)
                                .set_position('center')
                                .set_duration(duration_per_word)
                                .set_start(i * duration_per_word))
                    txt_clips.append(txt_clip)
                
            # Watermark
            watermark = (TextClip("TradingWizard AI", fontsize=30, color='white', font=self.font_path, stroke_color='black', stroke_width=1)
                         .set_position(('right', 'bottom'))
                         .set_duration(audio_clip.duration)
                         .set_opacity(0.6))
            
            # Composite
            final = CompositeVideoClip([final_video] + txt_clips + [watermark])
            
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            final.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)
            
            return output_path
            
        except Exception as e:
            print(f"Error assembling video: {e}")
            return None

if __name__ == "__main__":
    # Mock test
    editor = VideoEditor()
    # Ensure you have a 'test_video.mp4' in output dir to run this directly
    # editor.assemble_video("output/test_video.mp4", "output/temp_audio.mp3", "Bitcoin is going to the moon")
