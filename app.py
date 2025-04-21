import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import streamlit as st
from transcribe import transcribe_audio, download_youtube_audio
from summarize import summarize_text
from speak import speak_summary
from keywords import extract_keywords, analyze_sentiment
from transformers import pipeline
import json
from fpdf import FPDF

st.set_page_config(page_title="SmartCast Digestor", layout="wide")
st.title("🎙️ SmartCast Digestor")

# Choose input mode
mode = st.radio("Choose input source:", ["Upload audio file", "YouTube link"])

audio_path = None
transcript = None

if mode == "Upload audio file":
    uploaded = st.file_uploader("Upload your podcast (.mp3 or .wav)", type=["mp3", "wav"])
    if uploaded:
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded.read())
        audio_path = "temp_audio.wav"

elif mode == "YouTube link":
    youtube_url = st.text_input("Paste a YouTube video link (English speech works best)")
    if youtube_url:
        st.info("Downloading audio from YouTube...")
        audio_path = download_youtube_audio(youtube_url)
        st.success("Audio downloaded.")

# Proceed if audio is ready
if audio_path:
    st.info("Transcribing...")
    transcript = transcribe_audio(audio_path)
    st.text_area("Transcript", transcript, height=200)

    st.info("Summarizing...")
    summary = summarize_text(transcript)
    st.success("Summary:")
    st.write(summary)

    keywords = extract_keywords(summary)
    st.markdown("**Keywords:**")
    st.write(", ".join(keywords))

    sentiment = analyze_sentiment(summary)
    st.markdown("**Sentiment Analysis:**")
    st.json(sentiment)

    st.markdown("---")
    st.markdown("### ❓ Ask a Question About the Transcript")

    if "qa_pipeline" not in st.session_state:
        with st.spinner("Loading QA model..."):
            st.session_state.qa_pipeline = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad"
            )

    question = st.text_input("Ask your question:")
    if question:
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.qa_pipeline({
                    "context": transcript,
                    "question": question
                })
                st.success("Answer:")
                st.write(result["answer"])
            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.markdown("### 🧑‍🎤 Voice Style")
    voice_lang = st.selectbox(
        "Choose voice language/accent:",
        options=["en", "en-uk", "fr", "hi", "es"],
        format_func=lambda x: {
            "en": "English (US)",
            "en-uk": "English (UK)",
            "fr": "French 🇫🇷",
            "hi": "Hindi 🇮🇳",
            "es": "Spanish 🇪🇸"
        }.get(x, x)
    )

    st.info("Generating Voice...")
    audio_file = speak_summary(summary, lang=voice_lang)
    st.audio(audio_file)

    st.markdown("---")
    st.markdown("### 📥 Download Summary")

    data = {
        "Transcript": transcript,
        "Summary": summary,
        "Keywords": keywords,
        "Sentiment": sentiment
    }

    st.download_button("Download JSON", json.dumps(data, indent=2), "summary.json", "application/json")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Transcript:\n" + transcript + "\n\n")
    pdf.multi_cell(0, 10, "Summary:\n" + summary + "\n\n")
    pdf.multi_cell(0, 10, "Keywords:\n" + ", ".join(keywords) + "\n\n")
    pdf.multi_cell(0, 10, f"Sentiment:\n{sentiment}\n\n")
    pdf.output("summary.pdf")

    with open("summary.pdf", "rb") as f:
        st.download_button("Download PDF", f, "summary.pdf", "application/pdf")
