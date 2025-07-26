# Akıllı Sözleşme Asistanı

Bu proje, bir sözleşme metni üzerinden soruları yanıtlamak için Retrieval Augmented Generation (RAG) mimarisini kullanan bir sözleşme asistanıdır. Kullanıcı tarafından yüklenen bir PDF sözleşme dosyasını işler, içeriği parçalara ayırır, bu parçalardan vektörleştirmeler oluşturur ve bunları FAISS kullanarak bir vektör veritabanında saklar. Daha sonra, kullanıcı sorularını alır, FAISS veritabanından en alakalı bilgileri çeker ve Google Gemini 2.0 Flash modelini kullanarak bu bilgilere dayanarak yanıtlar üretir.

## Özellikler

- **PDF Metin Çıkarımı**: Yüklenen PDF sözleşme dosyalarından metin çıkarır.
- **Metin Parçalara Ayırma (Chunking)**: Uzun metinleri daha küçük, yönetilebilir parçalara ayırır.
- **Vektörleştirme (Embedding)**: Metin parçalarını `all-MiniLM-L6-v2` Sentence Transformer modeli kullanarak vektör temsillerine dönüştürür.
- **FAISS Vektör Veritabanı**: Hızlı ve verimli benzerlik aramaları için FAISS kullanarak vektör indeksleri oluşturur ve yönetir.
- **RAG Mimarisi**:
    - **Retrieval**: Kullanıcı sorgusunu vektörleştirir ve FAISS veritabanından en alakalı metin parçalarını alır.
    - **Augmentation**: Alınan bağlamı LLM'nin anlayabileceği bir formata dönüştürür.
    - **Generation**: Google Gemini 2.0 Flash modelini kullanarak alınan bağlama dayalı olarak kullanıcının sorusuna yanıt üretir.
- **Terminal Arayüzü**: Kullanıcıların sorularını girmesi ve asistanın yanıtlarını alması için basit bir komut satırı arayüzü sunar.

## Kurulum

1.  **Depoyu Klonlayın**:
    ```bash
    git clone <depo-url'niz>
    ```

2.  **Sanal Ortam Oluşturun ve Aktive Edin**:
    ```bash
    python -m venv venv

    # Windows
    .\venv\Scripts\activate

    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Gerekli Python Paketlerini Yükleyin**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Google API Anahtarını Yapılandırın**:
    * `.env` dosyasına Google Gemini API anahtarınızı ekleyin:
        
    * Google Gemini API anahtarınızı [Google AI Studio](https://aistudio.google.com/app/apikey) adresinden alabilirsiniz.

5.  **Sözleşme PDF Dosyasını Hazırlayın**:
    * Analiz etmek istediğiniz PDF sözleşme dosyasını projenizin ana dizinine `sozlesme.pdf` adıyla yerleştirin.

## Kullanım

### 1. Vektör Veritabanını Oluşturma

İlk olarak, sözleşme metninizden vektör veritabanını oluşturmanız gerekir. Bu adım, PDF'yi okur, parçalara ayırır, vektörleştirir ve FAISS indeksini kaydeder.

```bash
python vector_db.py
```

### 2. Akıllı Sözleşme Asistanını Çalıştırma

Vektör veritabanı oluşturulduktan sonra, ask_question.py betiğini çalıştırarak asistanı kullanmaya başlayabilirsiniz:

```bash
python ask_question.py
```

Asistan sizden bir soru girmenizi isteyecektir (İngilizce). Sorunuzu yazın ve Enter'a basın. Çıkmak için "exit" yazın.


## Dosya Açıklamaları

- [`ask_question.py`](ask_question.py): Kullanıcı sorularını işleyen, FAISS'ten bağlamı çeken ve Gemini modelini kullanarak yanıtlar üreten ana uygulama betiği.
- [`vector_db.py`](vector_db.py): PDF'den metin çıkarma, metni parçalara ayırma, embedding oluşturma ve FAISS vektör veritabanını oluşturup kaydetme işlemlerini gerçekleştiren betik.
- [`requirements.txt`](requirements.txt): Projenin bağımlılıklarını listeleyen dosya. 
    ```bash
    pip install -r requirements.txt
    ```
- [`.env`](.env): Google API anahtarını saklamak için kullanılan ortam değişkenleri dosyası.


## Notlar

- Bu asistan, sağlanan sözleşme metnine dayalı yanıtlar sağlar. Metinde olmayan veya çıkarılamayan bilgiler için yanıt veremeyebilir.
- Yanıtların doğruluğu, sağlanan bağlamın kalitesine ve Gemini modelinin performansına bağlıdır.
- Sorular İngilizce olarak girilmelidir.

