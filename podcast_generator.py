import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import re
from typing import Dict, List, Optional

class PodcastGenerator:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.generator = pipeline("text2text-generation", model="google/flan-t5-base")
        
    def generate_podcast_script(self, paper_data: Dict, style: str = "educational") -> str:
        """Generate a podcast-style script from scientific paper data."""
        
        sections = paper_data['sections']
        metadata = paper_data['metadata']
        findings = paper_data['findings']
        
        # Choose script template based on style
        if style == "educational":
            script = self._generate_educational_script(sections, metadata, findings)
        elif style == "storytelling":
            script = self._generate_storytelling_script(sections, metadata, findings)
        elif style == "interview":
            script = self._generate_interview_script(sections, metadata, findings)
        elif style == "news":
            script = self._generate_news_script(sections, metadata, findings)
        else:
            script = self._generate_educational_script(sections, metadata, findings)
        
        return script
    
    def _generate_educational_script(self, sections: Dict, metadata: Dict, findings: List[str]) -> str:
        """Generate an educational podcast script."""
        
        title = metadata.get('title', 'This Research Paper')
        year = metadata.get('year', 'recent')
        
        script_parts = []
        
        # Introduction
        intro = f"""
Welcome to Science Explained, where we break down complex research into digestible insights. 
Today, we're diving into a fascinating study titled "{title}" published in {year}.

Let me start by giving you the big picture of what this research is all about.
"""
        script_parts.append(intro)
        
        # Abstract summary
        if sections.get('abstract'):
            abstract_summary = self._summarize_for_podcast(sections['abstract'], "abstract")
            script_parts.append(f"""
Here's what the researchers set out to discover: {abstract_summary}
""")
        
        # Problem statement
        if sections.get('introduction'):
            intro_summary = self._summarize_for_podcast(sections['introduction'], "introduction")
            script_parts.append(f"""
The research addresses an important question: {intro_summary}
""")
        
        # Methods (simplified)
        if sections.get('methods'):
            methods_summary = self._summarize_for_podcast(sections['methods'], "methods")
            script_parts.append(f"""
So how did they go about answering this question? {methods_summary}
""")
        
        # Key findings
        if findings:
            script_parts.append("""
Now, here are the most important findings from this study:
""")
            for i, finding in enumerate(findings[:5], 1):
                script_parts.append(f"""
Finding number {i}: {finding}
""")
        
        # Results and implications
        if sections.get('results'):
            results_summary = self._summarize_for_podcast(sections['results'], "results")
            script_parts.append(f"""
The results tell us that: {results_summary}
""")
        
        # Discussion and implications
        if sections.get('discussion'):
            discussion_summary = self._summarize_for_podcast(sections['discussion'], "discussion")
            script_parts.append(f"""
What does this all mean? {discussion_summary}
""")
        
        # Conclusion
        conclusion = f"""
To wrap up today's episode, this research on "{title}" gives us valuable insights into 
an important area of study. The findings suggest that we need to pay attention to 
these results and consider their implications for future research and applications.

That's all for today's Science Explained. Thanks for listening, and remember, 
science is all around us - we just need to take the time to understand it.
"""
        script_parts.append(conclusion)
        
        return "\n".join(script_parts)
    
    def _generate_storytelling_script(self, sections: Dict, metadata: Dict, findings: List[str]) -> str:
        """Generate a storytelling podcast script."""
        
        title = metadata.get('title', 'This Research Paper')
        
        script_parts = []
        
        # Hook
        hook = f"""
Imagine you're a detective, and you've just been handed the most puzzling case of your career. 
That's exactly what happened to the researchers behind "{title}". 
They discovered something that made them scratch their heads and say, "Wait, that's not supposed to happen."

Today, I'm going to tell you the story of how they solved this scientific mystery.
"""
        script_parts.append(hook)
        
        # The problem
        if sections.get('introduction'):
            intro_summary = self._summarize_for_podcast(sections['introduction'], "introduction")
            script_parts.append(f"""
It all started when scientists noticed something strange: {intro_summary}
This was the beginning of a scientific journey that would take them down unexpected paths.
""")
        
        # The investigation
        if sections.get('methods'):
            methods_summary = self._summarize_for_podcast(sections['methods'], "methods")
            script_parts.append(f"""
Like any good detective story, they needed a plan. Here's how they investigated: {methods_summary}
""")
        
        # The discoveries
        if findings:
            script_parts.append("""
And then, the plot thickened. Here's what they discovered:
""")
            for i, finding in enumerate(findings[:5], 1):
                script_parts.append(f"""
Discovery {i}: {finding}
""")
        
        # The resolution
        if sections.get('results'):
            results_summary = self._summarize_for_podcast(sections['results'], "results")
            script_parts.append(f"""
Finally, the pieces of the puzzle came together: {results_summary}
""")
        
        # The moral of the story
        conclusion = f"""
And that's the story of "{title}". It's a reminder that in science, 
sometimes the most interesting discoveries come from asking the right questions 
and being willing to follow the evidence wherever it leads.

The next time you hear about a scientific breakthrough, remember that behind every 
discovery is a story of curiosity, persistence, and the thrill of uncovering something new.
"""
        script_parts.append(conclusion)
        
        return "\n".join(script_parts)
    
    def _generate_interview_script(self, sections: Dict, metadata: Dict, findings: List[str]) -> str:
        """Generate an interview-style podcast script."""
        
        title = metadata.get('title', 'This Research Paper')
        
        script_parts = []
        
        # Introduction
        intro = f"""
Welcome to Science Talk, where we interview the research itself. 
Today, we're sitting down with a fascinating study: "{title}".

Let me ask this research paper some questions to understand what it's all about.
"""
        script_parts.append(intro)
        
        # Q&A format
        if sections.get('abstract'):
            abstract_summary = self._summarize_for_podcast(sections['abstract'], "abstract")
            script_parts.append(f"""
Q: So, what's your main message? What should people know about you?

A: Well, let me tell you: {abstract_summary}
""")
        
        if sections.get('introduction'):
            intro_summary = self._summarize_for_podcast(sections['introduction'], "introduction")
            script_parts.append(f"""
Q: What problem were you trying to solve?

A: Great question! {intro_summary}
""")
        
        if sections.get('methods'):
            methods_summary = self._summarize_for_podcast(sections['methods'], "methods")
            script_parts.append(f"""
Q: How did you go about finding answers?

A: Here's my approach: {methods_summary}
""")
        
        if findings:
            script_parts.append("""
Q: What are your most important findings?

A: I'm glad you asked! Here are my key discoveries:
""")
            for i, finding in enumerate(findings[:5], 1):
                script_parts.append(f"""
{i}. {finding}
""")
        
        if sections.get('results'):
            results_summary = self._summarize_for_podcast(sections['results'], "results")
            script_parts.append(f"""
Q: What do your results tell us?

A: My results show that: {results_summary}
""")
        
        # Closing
        closing = f"""
Q: What's your takeaway message for our listeners?

A: I want people to understand that "{title}" represents an important step forward 
in our understanding of this field. The implications are significant, and I hope 
this research inspires others to build upon these findings.

That concludes our interview with "{title}". Thanks for sharing your insights with us!
"""
        script_parts.append(closing)
        
        return "\n".join(script_parts)
    
    def _generate_news_script(self, sections: Dict, metadata: Dict, findings: List[str]) -> str:
        """Generate a news-style podcast script."""
        
        title = metadata.get('title', 'This Research Paper')
        year = metadata.get('year', 'recent')
        
        script_parts = []
        
        # Headline
        headline = f"""
BREAKING SCIENCE NEWS: "{title}" - New Research Reveals Surprising Findings

This is Science News Daily, bringing you the latest developments in scientific research.
"""
        script_parts.append(headline)
        
        # Lead
        if sections.get('abstract'):
            abstract_summary = self._summarize_for_podcast(sections['abstract'], "abstract")
            script_parts.append(f"""
In a groundbreaking study published in {year}, researchers have made a significant discovery: {abstract_summary}
""")
        
        # Background
        if sections.get('introduction'):
            intro_summary = self._summarize_for_podcast(sections['introduction'], "introduction")
            script_parts.append(f"""
The research addresses a critical issue: {intro_summary}
""")
        
        # Key findings
        if findings:
            script_parts.append("""
Here are the major findings from this study:
""")
            for i, finding in enumerate(findings[:5], 1):
                script_parts.append(f"""
• {finding}
""")
        
        # Impact
        if sections.get('discussion'):
            discussion_summary = self._summarize_for_podcast(sections['discussion'], "discussion")
            script_parts.append(f"""
The implications of this research are significant: {discussion_summary}
""")
        
        # Sign off
        signoff = f"""
This has been Science News Daily. The study "{title}" represents an important 
contribution to the field and will likely influence future research directions.

Stay tuned for more breaking science news. This is Science News Daily, 
keeping you informed about the latest discoveries that shape our world.
"""
        script_parts.append(signoff)
        
        return "\n".join(script_parts)
    
    def _summarize_for_podcast(self, text: str, section_type: str) -> str:
        """Generate podcast-friendly summaries of paper sections."""
        
        # Clean and chunk the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) < 200:
            return text
        
        # Create chunks for summarization
        chunks = [text[i:i+800] for i in range(0, len(text), 800)]
        
        summaries = []
        for chunk in chunks:
            try:
                result = self.summarizer(chunk, max_length=150, min_length=30, do_sample=False)
                summaries.append(result[0]['summary_text'])
            except Exception as e:
                # Fallback: use first few sentences
                sentences = re.split(r'[.!?]+', chunk)
                summaries.append('. '.join(sentences[:3]) + '.')
        
        return ' '.join(summaries)
    
    def generate_episode_metadata(self, paper_data: Dict, script: str) -> Dict:
        """Generate metadata for the podcast episode."""
        
        metadata = paper_data['metadata']
        sections = paper_data['sections']
        
        # Estimate episode duration (average speaking rate: 150 words per minute)
        word_count = len(script.split())
        duration_minutes = max(3, word_count // 150)  # Minimum 3 minutes
        
        # Generate episode title
        if metadata.get('title'):
            episode_title = f"Breaking Down: {metadata['title']}"
        else:
            episode_title = "Scientific Paper Analysis"
        
        # Generate description
        if sections.get('abstract'):
            description = self._summarize_for_podcast(sections['abstract'], "abstract")
        else:
            description = "A detailed analysis of a scientific research paper, breaking down complex concepts into understandable insights."
        
        return {
            'episode_title': episode_title,
            'duration_minutes': duration_minutes,
            'word_count': word_count,
            'description': description,
            'paper_title': metadata.get('title', 'Unknown'),
            'paper_year': metadata.get('year', 'Unknown'),
            'paper_doi': metadata.get('doi', '')
        }

def create_podcast_from_paper(paper_data: Dict, style: str = "educational") -> Dict:
    """Main function to create a podcast from scientific paper data."""
    
    generator = PodcastGenerator()
    
    # Generate the script
    script = generator.generate_podcast_script(paper_data, style)
    
    # Generate episode metadata
    metadata = generator.generate_episode_metadata(paper_data, script)
    
    return {
        'script': script,
        'metadata': metadata,
        'style': style
    } 