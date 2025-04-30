import whisper
import yt_dlp
import os

def download_youtube_audio(url, filename="youtube_audio"):
    output_path = f"{filename}.mp3"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,  # No extension here!
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # Upgrade to 'medium' if you're feeling powerful
    result = model.transcribe(audio_path)
    return result["text"]
