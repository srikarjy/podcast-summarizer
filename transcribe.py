import whisper
import yt_dlp
import os

def download_youtube_audio(url, filename="youtube_audio"):
    # Output template uses yt-dlp's dynamic extension feature
    output_template = f"{filename}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # We expect yt-dlp to convert and save as mp3
    expected_file = f"{filename}.mp3"
    if not os.path.exists(expected_file):
        raise FileNotFoundError(f"Expected audio file not found: {expected_file}")
    
    return expected_file

def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # Try 'medium' or 'large' if your laptop is made of dragon scales
    result = model.transcribe(audio_path)
    return result["text"]
