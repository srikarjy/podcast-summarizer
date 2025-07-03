import base64

audio_data = b"""
SUQzAwAAAAAAflRFTkMAAAAUAAADTGF2ZjU4LjM3LjEwMAAAAAAAAAAAAAAA//tQxAADBzAAAAANIAAAAAExBTUUz
LjEwMAAAAAAAAAAAAAAA//ugxAAL0gAABAAADugAAAB9AAACABFzcGVlY2gudGVzdAAAAAABcQAAAAAAABEIAMsA
AACAGkxhdmM1OC4yNi4xMABUZXN0aW5nIFdoaXNwZXIgZnJvbSBNb25kYXkuIEFpIGlzIGNvb2wu
"""

with open("sample_audio/test_podcast.mp3", "wb") as f:
    f.write(base64.b64decode(audio_data))

print("✅ Audio file saved as sample_audio/test_podcast.mp3")
