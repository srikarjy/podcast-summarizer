# SmartCast Digestor - Scientific Paper to Podcast Converter

SmartCast Digestor transforms scientific papers into podcast-style explanations. This application processes scientific papers (PDF or arXiv) and generates educational, storytelling, interview-style, or news-format podcast scripts with audio narration.

## Features

### Scientific Paper Processing
- PDF Upload: Upload any scientific paper in PDF format
- arXiv Integration: Direct processing of arXiv papers via URL or ID
- Smart Text Extraction: Advanced PDF parsing with multiple fallback methods
- Section Analysis: Automatic extraction of Abstract, Introduction, Methods, Results, Discussion, and Conclusion
- Key Findings Detection: AI-powered identification of important research findings

### Podcast Generation
- Four Podcast Styles:
  - Educational: Academic explanation with clear structure
  - Storytelling: Narrative approach with engaging story elements
  - Interview: Q&A format simulating an interview with the research
  - News: Breaking news style reporting

### Multilingual Support
- Generate podcasts in multiple languages:
  - English (US and UK)
  - French
  - Hindi
  - Spanish

### Advanced Analytics
- Paper Metadata Extraction: Title, authors, year, DOI
- Key Findings Analysis: Important statements and conclusions
- Question Answering: Ask specific questions about the paper
- Episode Metadata: Duration, word count, and descriptions

## Quick Start

### Installation

1. Install Dependencies:
```
pip install -r requirements.txt
```

2. Run the Application:
```
streamlit run app.py
```

### Usage

1. Choose Input Source: Select "Scientific Paper" from the radio buttons
2. Upload Paper: Either upload a PDF file or provide an arXiv URL/ID
3. Select Podcast Style: Choose from Educational, Storytelling, Interview, or News format
4. Generate Podcast: Click "Generate Podcast Script" to create the explanation
5. Download Results: Get the script, audio files, and metadata in various formats

## Example Usage

### Processing an arXiv Paper
```
Input: https://arxiv.org/abs/1706.03762
Style: Educational
Output: Podcast explaining "Attention Is All You Need"
```

### Processing a PDF Upload
```
Input: research_paper.pdf
Style: Storytelling
Output: Narrative podcast about the research journey
```

## Technical Architecture

### Core Components

1. `paper_processor.py`: Handles PDF extraction and paper analysis
   - PyMuPDF and PyPDF2 for robust text extraction
   - arXiv API integration
   - Section detection and metadata extraction
   - Key findings identification

2. `podcast_generator.py`: Creates podcast scripts
   - Multiple narrative styles
   - AI-powered summarization
   - Episode metadata generation
   - Duration estimation

3. `app.py`: Main Streamlit interface
   - Unified interface for audio and paper processing
   - Real-time processing with progress indicators
   - Multiple export formats

### Supported Formats

- Input: PDF files, arXiv URLs/IDs
- Output: 
  - Audio files (MP3)
  - Text scripts (TXT)
  - Metadata (JSON)
  - Reports (PDF)

## Use Cases

### For Researchers
- Paper Summaries: Quickly understand complex research
- Teaching Materials: Create educational content from papers
- Collaboration: Share research insights in accessible formats

### For Students
- Study Aids: Convert dense papers into digestible content
- Language Learning: Practice with scientific content in multiple languages
- Research Skills: Learn to extract key information from papers

### For Educators
- Course Content: Create engaging explanations for students
- Multilingual Teaching: Generate content in different languages
- Assessment: Use generated content for quizzes and discussions

### For Science Communicators
- Content Creation: Generate podcast episodes from recent research
- Public Engagement: Make complex science accessible to general audiences
- Multilingual Outreach: Reach global audiences

## Advanced Features

### Question Answering
Ask specific questions about the paper and get AI-powered answers based on the content.

### Section Analysis
View extracted sections (Abstract, Methods, Results, etc.) for detailed analysis.

### Key Findings
Automatically identify and highlight the most important statements from the research.

### Episode Metadata
Get detailed information about generated episodes including duration, word count, and descriptions.

## File Structure

```
srikar_finalproject_podcast-summarizer/
├── app.py                 # Main Streamlit application
├── paper_processor.py     # Scientific paper processing
├── podcast_generator.py   # Podcast script generation
├── transcribe.py          # Audio transcription (existing)
├── summarize.py           # Text summarization (existing)
├── speak.py               # Text-to-speech (existing)
├── keywords.py            # Keyword extraction (existing)
├── translate.py           # Translation (existing)
├── sample_paper.py        # Sample paper generator
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Podcast Styles Explained

### Educational Style
- Structure: Academic explanation with clear sections
- Tone: Professional and informative
- Best for: Students, researchers, formal presentations
- Example: "Welcome to Science Explained, where we break down complex research..."

### Storytelling Style
- Structure: Narrative with beginning, middle, and end
- Tone: Engaging and conversational
- Best for: General audiences, public engagement
- Example: "Imagine you're a detective, and you've just been handed the most puzzling case..."

### Interview Style
- Structure: Q&A format with the research as the interviewee
- Tone: Conversational and interactive
- Best for: Podcasts, radio shows, interactive learning
- Example: "Q: So, what's your main message? A: Well, let me tell you..."

### News Style
- Structure: Breaking news format with headlines and impact
- Tone: Urgent and informative
- Best for: Science news, current events, rapid dissemination
- Example: "Breaking science news: New research reveals surprising findings..."

## Future Enhancements

- More Languages: Additional language support
- Voice Customization: Different voice styles and speeds
- Interactive Elements: Clickable timestamps and sections
- Batch Processing: Process multiple papers at once
- Advanced Analytics: More detailed paper analysis
- Integration: Connect with academic databases
- Mobile App: Native mobile application
- API Access: REST API for programmatic access

## Contributing

Contributions are welcome. You can help by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding new podcast styles
- Enhancing language support

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Transformers Library: For AI models and pipelines
- Streamlit: For the web interface
- PyMuPDF: For advanced PDF processing
- arXiv: For scientific paper access
- gTTS: For text-to-speech capabilities

SmartCast Digestor helps you turn scientific papers into accessible podcasts for research, education, and public communication. 