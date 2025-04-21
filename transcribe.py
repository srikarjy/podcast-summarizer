import whisper
import yt_dlp
import os

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

def download_youtube_audio(url, output_path="temp_audio.wav"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for ext in ["webm", "m4a", "mp3", "wav"]:
        if os.path.exists(f"temp_audio.{ext}"):
            os.rename(f"temp_audio.{ext}", output_path)
            break
    return output_path
