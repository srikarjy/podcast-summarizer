import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import streamlit as st
from transcribe import transcribe_audio, download_youtube_audio
from summarize import summarize_text
from speak import speak_summary
from keywords import extract_keywords, analyze_sentiment
from translate import translate_text
from paper_processor import process_paper_input
from podcast_generator import create_podcast_from_paper
from transformers import pipeline
import json
from fpdf import FPDF

st.set_page_config(page_title="SmartCast Digestor", layout="wide")
st.title("🎙️ SmartCast Digestor")

# Choose input mode
mode = st.radio("Choose input source:", ["Upload audio file", "YouTube link", "Scientific Paper"])

audio_path = None
transcript = None
paper_data = None

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

elif mode == "Scientific Paper":
    st.markdown("### 📄 Scientific Paper Processing")
    
    paper_input_type = st.radio("Choose paper input method:", ["Upload PDF", "arXiv URL/ID"])
    
    if paper_input_type == "Upload PDF":
        uploaded_pdf = st.file_uploader("Upload scientific paper (PDF)", type=["pdf"])
        if uploaded_pdf:
            with open("temp_paper.pdf", "wb") as f:
                f.write(uploaded_pdf.read())
            
            with st.spinner("Processing scientific paper..."):
                try:
                    text, paper_data = process_paper_input("temp_paper.pdf")
                    st.success("Paper processed successfully!")
                    
                    # Display paper metadata
                    if paper_data['metadata'].get('title'):
                        st.markdown(f"**Paper Title:** {paper_data['metadata']['title']}")
                    if paper_data['metadata'].get('year'):
                        st.markdown(f"**Year:** {paper_data['metadata']['year']}")
                    if paper_data['metadata'].get('doi'):
                        st.markdown(f"**DOI:** {paper_data['metadata']['doi']}")
                    
                except Exception as e:
                    st.error(f"Error processing paper: {str(e)}")
    
    else:  # arXiv URL/ID
        arxiv_input = st.text_input("Enter arXiv URL or ID (e.g., https://arxiv.org/abs/2103.12345 or 2103.12345)")
        if arxiv_input:
            with st.spinner("Downloading and processing arXiv paper..."):
                try:
                    text, paper_data = process_paper_input(arxiv_input)
                    st.success("Paper processed successfully!")
                    
                    # Display paper metadata
                    if paper_data['metadata'].get('title'):
                        st.markdown(f"**Paper Title:** {paper_data['metadata']['title']}")
                    if paper_data['metadata'].get('year'):
                        st.markdown(f"**Year:** {paper_data['metadata']['year']}")
                    if paper_data['metadata'].get('doi'):
                        st.markdown(f"**DOI:** {paper_data['metadata']['doi']}")
                    
                except Exception as e:
                    st.error(f"Error processing arXiv paper: {str(e)}")

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
        with st.spinner("Loading upgraded QA model..."):
            st.session_state.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/xlm-roberta-base-squad2",
                tokenizer="deepset/xlm-roberta-base-squad2"
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
    voice_langs = st.multiselect(
        "Choose voice languages:",
        options=["en", "en-uk", "fr", "hi", "es"],
        default=["en"],
        format_func=lambda x: {
            "en": "English (US)",
            "en-uk": "English (UK)",
            "fr": "French 🇫🇷",
            "hi": "Hindi 🇮🇳",
            "es": "Spanish 🇪🇸"
        }.get(x, x)
    )

    for lang in voice_langs:
        st.markdown(f"### 🔊 Audio Summary in {lang.upper()}")
        if lang in ["hi", "fr", "es"]:
            translated_summary = translate_text(summary, src_lang="en", tgt_lang=lang)
        else:
            translated_summary = summary

        audio_file = speak_summary(translated_summary, lang=lang)
        st.audio(audio_file)

        with open(audio_file, "rb") as f:
            st.download_button(
                label=f"Download {lang.upper()} Audio",
                data=f,
                file_name=f"summary_{lang}.mp3",
                mime="audio/mpeg"
            )

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

# Process scientific paper input (new functionality)
elif paper_data:
    st.markdown("---")
    st.markdown("### 📊 Paper Analysis")
    
    # Display extracted sections
    with st.expander("📖 Paper Sections"):
        sections = paper_data['sections']
        for section_name, content in sections.items():
            if content.strip():
                st.markdown(f"**{section_name.title()}:**")
                st.text_area(f"{section_name.title()} Content", content, height=150, key=f"section_{section_name}")
    
    # Display key findings
    if paper_data['findings']:
        st.markdown("### 🔍 Key Findings")
        for i, finding in enumerate(paper_data['findings'], 1):
            st.markdown(f"**{i}.** {finding}")
    
    st.markdown("---")
    st.markdown("### 🎙️ Generate Podcast Explanation")
    
    # Podcast style selection
    podcast_style = st.selectbox(
        "Choose podcast style:",
        ["educational", "storytelling", "interview", "news"],
        format_func=lambda x: {
            "educational": "🎓 Educational (Academic explanation)",
            "storytelling": "📖 Storytelling (Narrative approach)",
            "interview": "🎤 Interview (Q&A format)",
            "news": "📰 News (Breaking news style)"
        }.get(x, x)
    )
    
    if st.button("🎙️ Generate Podcast Script"):
        with st.spinner("Generating podcast script..."):
            try:
                podcast_result = create_podcast_from_paper(paper_data, podcast_style)
                
                st.markdown("### 📝 Generated Podcast Script")
                st.text_area("Podcast Script", podcast_result['script'], height=400)
                
                # Display episode metadata
                metadata = podcast_result['metadata']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Episode Duration", f"{metadata['duration_minutes']} min")
                with col2:
                    st.metric("Word Count", metadata['word_count'])
                with col3:
                    st.metric("Style", podcast_style.title())
                
                st.markdown(f"**Episode Title:** {metadata['episode_title']}")
                st.markdown(f"**Description:** {metadata['description']}")
                
                # Generate audio from script
                st.markdown("### 🔊 Generate Audio Podcast")
                voice_langs = st.multiselect(
                    "Choose voice languages for podcast:",
                    options=["en", "en-uk", "fr", "hi", "es"],
                    default=["en"],
                    format_func=lambda x: {
                        "en": "English (US)",
                        "en-uk": "English (UK)",
                        "fr": "French 🇫🇷",
                        "hi": "Hindi 🇮🇳",
                        "es": "Spanish 🇪🇸"
                    }.get(x, x)
                )
                
                for lang in voice_langs:
                    st.markdown(f"### 🔊 Podcast Audio in {lang.upper()}")
                    
                    # For non-English languages, translate the script
                    if lang in ["hi", "fr", "es"]:
                        translated_script = translate_text(podcast_result['script'], src_lang="en", tgt_lang=lang)
                    else:
                        translated_script = podcast_result['script']
                    
                    audio_file = speak_summary(translated_script, lang=lang)
                    st.audio(audio_file)
                    
                    with open(audio_file, "rb") as f:
                        st.download_button(
                            label=f"Download {lang.upper()} Podcast",
                            data=f,
                            file_name=f"podcast_{podcast_style}_{lang}.mp3",
                            mime="audio/mpeg"
                        )
                
                # Download options
                st.markdown("---")
                st.markdown("### 📥 Download Podcast")
                
                # Download script as text
                st.download_button(
                    "Download Script (TXT)",
                    podcast_result['script'],
                    file_name=f"podcast_script_{podcast_style}.txt",
                    mime="text/plain"
                )
                
                # Download metadata as JSON
                podcast_data = {
                    "script": podcast_result['script'],
                    "metadata": podcast_result['metadata'],
                    "style": podcast_style,
                    "paper_metadata": paper_data['metadata'],
                    "key_findings": paper_data['findings']
                }
                
                st.download_button(
                    "Download Full Data (JSON)",
                    json.dumps(podcast_data, indent=2),
                    file_name=f"podcast_data_{podcast_style}.json",
                    mime="application/json"
                )
                
                # Generate PDF report
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Podcast Script: {metadata['episode_title']}\n\n")
                pdf.multi_cell(0, 10, f"Style: {podcast_style.title()}\n")
                pdf.multi_cell(0, 10, f"Duration: {metadata['duration_minutes']} minutes\n")
                pdf.multi_cell(0, 10, f"Word Count: {metadata['word_count']}\n\n")
                pdf.multi_cell(0, 10, "Script:\n" + podcast_result['script'] + "\n\n")
                pdf.multi_cell(0, 10, f"Original Paper: {metadata['paper_title']}\n")
                pdf.multi_cell(0, 10, f"Year: {metadata['paper_year']}\n")
                if metadata['paper_doi']:
                    pdf.multi_cell(0, 10, f"DOI: {metadata['paper_doi']}\n")
                pdf.output("podcast_script.pdf")
                
                with open("podcast_script.pdf", "rb") as f:
                    st.download_button(
                        "Download Script (PDF)",
                        f,
                        file_name=f"podcast_script_{podcast_style}.pdf",
                        mime="application/pdf"
                    )
                
            except Exception as e:
                st.error(f"Error generating podcast: {str(e)}")
    
    # Question answering for papers
    st.markdown("---")
    st.markdown("### ❓ Ask Questions About the Paper")
    
    if "qa_pipeline" not in st.session_state:
        with st.spinner("Loading QA model..."):
            st.session_state.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/xlm-roberta-base-squad2",
                tokenizer="deepset/xlm-roberta-base-squad2"
            )
    
    question = st.text_input("Ask a question about the paper:")
    if question:
        with st.spinner("Analyzing..."):
            try:
                result = st.session_state.qa_pipeline({
                    "context": paper_data['full_text'],
                    "question": question
                })
                st.success("Answer:")
                st.write(result["answer"])
            except Exception as e:
                st.error(f"Error: {str(e)}")
