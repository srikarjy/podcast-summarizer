import yake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def extract_keywords(text, max_keywords=10):
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords[:max_keywords]]

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)
