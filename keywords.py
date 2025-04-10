# keywords.py
from keybert import KeyBERT

kw_model = KeyBERT()

def extract_keywords(text, top_n=5):
    keywords = kw_model.extract_keywords(text, stop_words='english', top_n=top_n)
    return [kw[0] for kw in keywords]
