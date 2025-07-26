"""
Faiss kullanarak vektör veri tabanı oluşturma ve sorgulama işlemlerini gerçekleştiren modül.
"""

import os
import fitz
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

### Dosya formatı PDF olarak varsayılmıştır. PDF -> TEXT
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    return text

# print(extract_text_from_pdf("sozlesme.pdf"))

### Metni daha küçük parçalara ayırma
def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

### Sentence transformer ile embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

pdf_file_path = "sozlesme.pdf"

text = extract_text_from_pdf(pdf_file_path)
chunks = split_text_into_chunks(text)
embeddings = model.encode(chunks)

# print(f"Embedding boyutu: {embeddings.shape}")

### Faiss index oluşturma
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

os.makedirs("data", exist_ok=True)
faiss.write_index(index, "data/contract_index.faiss")
with open("data/contract_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Faiss index ve chunk'lar kaydedildi.")



















