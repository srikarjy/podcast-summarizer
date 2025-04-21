from gtts import gTTS

def speak_summary(text, lang="en"):
    real_lang = lang if lang != "en-uk" else "en"
    tts = gTTS(text, lang=real_lang, tld="co.uk" if lang == "en-uk" else "com")
    filename = "summary.mp3"
    tts.save(filename)
    return filename
