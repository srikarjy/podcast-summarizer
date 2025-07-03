import PyPDF2
import fitz  # PyMuPDF
import arxiv
import requests
from bs4 import BeautifulSoup
import re
import os
from typing import Dict, List, Optional, Tuple

class ScientificPaperProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt']
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file using multiple methods for better results."""
        text = ""
        
        # Method 1: PyMuPDF (better for complex layouts)
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            print(f"PyMuPDF failed: {e}")
        
        # Method 2: PyPDF2 (fallback)
        if not text.strip():
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"PyPDF2 failed: {e}")
        
        return text.strip()
    
    def download_arxiv_paper(self, arxiv_id: str) -> str:
        """Download and extract text from arXiv paper."""
        try:
            # Search for the paper
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(search.results())
            
            # Download PDF
            paper.download_pdf(filename=f"temp_{arxiv_id}.pdf")
            
            # Extract text
            text = self.extract_text_from_pdf(f"temp_{arxiv_id}.pdf")
            
            # Clean up
            os.remove(f"temp_{arxiv_id}.pdf")
            
            return text
        except Exception as e:
            raise Exception(f"Failed to download arXiv paper: {e}")
    
    def extract_paper_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections of a scientific paper."""
        sections = {
            'title': '',
            'abstract': '',
            'introduction': '',
            'methods': '',
            'results': '',
            'discussion': '',
            'conclusion': '',
            'references': ''
        }
        
        # Common section headers
        section_patterns = {
            'abstract': r'(?i)(abstract|summary)',
            'introduction': r'(?i)(introduction|intro)',
            'methods': r'(?i)(methods|methodology|materials and methods|experimental)',
            'results': r'(?i)(results|findings)',
            'discussion': r'(?i)(discussion|discuss)',
            'conclusion': r'(?i)(conclusion|conclusions|summary)',
            'references': r'(?i)(references|bibliography|citations)'
        }
        
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is a section header
            found_section = None
            for section_name, pattern in section_patterns.items():
                if re.match(pattern, line, re.IGNORECASE):
                    found_section = section_name
                    break
            
            if found_section:
                # Save previous section content
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = found_section
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers
        text = re.sub(r'\b\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]]+', ' ', text)
        
        return text.strip()
    
    def extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings and important statements from the paper."""
        findings = []
        
        # Look for sentences with key phrases
        key_phrases = [
            r'we found',
            r'results show',
            r'study demonstrates',
            r'analysis reveals',
            r'significant',
            r'important',
            r'key finding',
            r'conclusion',
            r'implication'
        ]
        
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue
                
            for phrase in key_phrases:
                if re.search(phrase, sentence, re.IGNORECASE):
                    findings.append(sentence)
                    break
        
        return findings[:10]  # Return top 10 findings
    
    def get_paper_metadata(self, text: str) -> Dict[str, str]:
        """Extract basic metadata from the paper."""
        metadata = {
            'title': '',
            'authors': '',
            'journal': '',
            'year': '',
            'doi': ''
        }
        
        lines = text.split('\n')
        
        # Try to find title (usually first few lines)
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            if len(line) > 10 and len(line) < 200 and not line.isupper():
                metadata['title'] = line
                break
        
        # Look for DOI
        doi_match = re.search(r'doi:?\s*([^\s]+)', text, re.IGNORECASE)
        if doi_match:
            metadata['doi'] = doi_match.group(1)
        
        # Look for year
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        if year_match:
            metadata['year'] = year_match.group(0)
        
        return metadata

def process_paper_input(input_source: str) -> Tuple[str, Dict]:
    """Main function to process paper input (file upload or arXiv ID)."""
    processor = ScientificPaperProcessor()
    
    if input_source.startswith('http') or input_source.startswith('arxiv.org'):
        # Extract arXiv ID from URL
        arxiv_id = input_source.split('/')[-1]
        if arxiv_id.startswith('abs/'):
            arxiv_id = arxiv_id[4:]
        text = processor.download_arxiv_paper(arxiv_id)
    else:
        # Assume it's a file path
        if not os.path.exists(input_source):
            raise FileNotFoundError(f"File not found: {input_source}")
        text = processor.extract_text_from_pdf(input_source)
    
    # Clean the text
    text = processor.clean_text(text)
    
    # Extract sections
    sections = processor.extract_paper_sections(text)
    
    # Extract metadata
    metadata = processor.get_paper_metadata(text)
    
    # Extract key findings
    findings = processor.extract_key_findings(text)
    
    return text, {
        'sections': sections,
        'metadata': metadata,
        'findings': findings,
        'full_text': text
    } 