# semantic_search.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

class SemanticSearch:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add_texts(self, texts):
        embeddings = model.encode(texts)
        self.index.add(np.array(embeddings).astype('float32'))
        self.texts.extend(texts)

    def search(self, query, top_k=3):
        query_embedding = model.encode([query]).astype('float32')
        D, I = self.index.search(query_embedding, top_k)
        return [self.texts[i] for i in I[0]]
