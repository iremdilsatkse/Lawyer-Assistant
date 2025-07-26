"""
Kullanıcı için sözleşme asistanı.
    - Kullanıcının yüklediği bir sözleşmeden özet çıkarabilir.
    - Faiss kullanarak hızlı arama yapabilen vektör veri tabanı var.
    - Kullanıcının sorularını alıp, veri tabanından bilgi getirip GEMINI ile cevaplar.

Embedding, Faiss ve GEMINI kullanılan teknolojilerdir.
"""
"""
RAG mimarisine sahip. 
Kullanıcı sorularını alır, veri tabanından bilgi getirir ve GEMINI ile cevaplar.
    - Retrieval ile kullanıcı sorusu embedding'e dönüştürülür, faiss üzerinden en alakalı chunk getirilir.
    - Augmentation ile LLM alayacak şekilde bir formata dönüştürülür.
    - Generation ile cevap oluşturulur.
"""
import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import numpy as np

import google.generativeai as genai

# .env dosyasından API anahtarını yükleme
load_dotenv()

# Google API anahtarını ayarla
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Faiss index ve chunkları yükleme
index = faiss.read_index("data/contract_index.faiss")

# Chunklanmış verinin yüklenmesi
with open ("data/contract_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Kullanıcıdan gelen soruları alma
while True:
    question = input("\n Sorunuzu girin (İngilizce):")
    if question.lower() == "exit":
        print("Çıkılıyor...")
        break

    # kullanıcı sorusunu embedding'e dönüştürme
    question_embedding = model.encode([question])

    # faiss veri tabanından en yakın 3 chunk'ı alma
    k = 3
    distances, indices = index.search(np.array(question_embedding), k)

    # bulunan chunk'ları birleştirme
    retrieved_chunks = [chunks[i] for i in indices[0]]
    context = "\n ----- \n".join(retrieved_chunks)

    prompt = f"""
            You are a contract assistant. Your task is to answer questions based on the provided contract text.

            Context: 
            {context}

            Question:
            {question}

            Answer:

    """

    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
    response = gemini_model.generate_content(prompt, generation_config={"temperature": 0.2})

    print("AI Assistant: \n", response.text.strip())















