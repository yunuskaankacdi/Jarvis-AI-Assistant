# Jarvis - Local LLM & Web UI Destekli Kişisel Asistan 🤖

Python tabanlı, cihaz tespiti yapabilen ve sesli/yazılı komutlarla çalışan akıllı otomasyon asistanı. 

Sistem sıradan bir API bağlantısı yerine arka planda **Ollama** aracılığıyla yerel bir büyük dil modeli (Llama 3) çalıştırır. Bu sayede veri gizliliği maksimumda tutulurken, Flask altyapısıyla geliştirilen Web Arayüzü (Web UI) üzerinden kolayca kontrol edilebilir.

### 🚀 Özellikler
* **Local LLM Entegrasyonu:** Llama 3 ile tamamen yerel (offline) yapay zeka sohbeti.
* **Flask Web UI:** Terminale bağlı kalmadan tarayıcı üzerinden kontrol sağlayan modern arayüz.
* **Dinamik Otomasyon:** Web scraping ve komut analizi ile platform algılama (Örn: "YouTube'u aç").
* **Cihaz Karar Yapısı:** Hedef bağlantıları açmadan önce PC/Mobil cihaz teyidi alma mekanizması.
* **Sesli Etkileşim:** Microsoft Edge TTS ile doğal ve akıcı sesli yanıt sistemi (Ahmet Neural).

### 🛠️ Kullanılan Teknolojiler
* **Dil & Çatı:** Python, Flask
* **Yapay Zeka & LLM:** Ollama (Llama 3), OpenAI (Base URL yönlendirmesi ile)
* **Ses İşleme:** SpeechRecognition (STT), Edge-TTS & Pygame (TTS)

---

### ⚙️ Kurulum ve Çalıştırma Yönergesi

**ÖNEMLİ:** Projenin yapay zeka cevapları üretebilmesi için bilgisayarınızda **Ollama** kurulu ve arka planda çalışıyor olmalıdır.

1. **Ollama'yı Hazırlayın:**
   * [Ollama resmi sitesinden](https://ollama.com/) uygulamayı indirip kurun.
   * Terminal veya Komut İstemini (CMD) açıp şu komutu çalıştırarak Llama 3 modelini indirin:
     ```bash
     ollama run llama3
     ```
   * *Not: Bu komut arka planda localhost:11434 portunda yerel AI sunucusunu başlatacaktır.*

2. **Gerekli Python Kütüphanelerini Kurun:**
   ```bash
   pip install flask openai speechrecognition edge-tts pygame pymupdf
