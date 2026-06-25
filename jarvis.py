import speech_recognition as sr
import edge_tts
import asyncio
import pygame
import os 
import webbrowser
from openai import OpenAI
import fitz
from flask import Flask, render_template, request, jsonify
import threading

pygame.mixer.init()

# Web sunucusunu başlatıyoruz
app = Flask(__name__)

# Yerel Ollama (Llama 3) bağlantısı
client = OpenAI(base_url="http://localhost:11434/v1", api_key="bedava-jarvis")

def konus(metin):
    """Metni Microsoft'un ultra gerçekçi Neural AI sesiyle okur."""
    ses_dosyasi = "jarvis_ses.mp3"
    
    async def ses_olustur():
        communicate = edge_tts.Communicate(metin, "tr-TR-AhmetNeural", rate="+10%")
        await communicate.save(ses_dosyasi)
    
    asyncio.run(ses_olustur())
    
    try:
        pygame.mixer.music.load(ses_dosyasi)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Ses çalma hatası: {e}")
    finally:
        if os.path.exists(ses_dosyasi):
            try:
                os.remove(ses_dosyasi)
            except:
                pass

def dinle():
    r = sr.Recognizer()
    r.pause_threshold = 1.3
    
    with sr.Microphone() as source:
        print("\nDinliyorum...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        
    try:
        komut = r.recognize_google(audio, language='tr-TR').lower()
        
        duzeltmeler = {
            "doğan": "şu an",
            "şuan": "şu an",
            "jaris": "jarvis",
            "cervis": "jarvis"
        }
        
        for yanlis, dogru in duzeltmeler.items():
            komut = komut.replace(yanlis, dogru)
            
        print(f"Sen: {komut}")
        return komut
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def yapay_zeka_yaniti(metin):
    try:
        response = client.chat.completions.create(
            model="llama3",
            messages=[
                {"role": "system", "content": "Sen bir bilgisayar asistanısın. Adın Jarvis. Lütfen sorulara her zaman Türkçe ve çok kısa, net yanıtlar ver."},
                {"role": "user", "content": metin}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Yapay zeka motoruna ulaşılamıyor. Lütfen yerel sunucuyu kontrol edin."

def pdf_oku(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        return "Okunacak PDF dosyası bulunamadı."
    try:
        doc = fitz.open(dosya_yolu)
        metin = ""
        for sayfa in doc:
            metin += sayfa.get_text()
        return metin
    except Exception as e:
        return f"Hata: {str(e)}"

def hedef_site_bul(komut):
    """Gelen komutun içindeki platformu tespit eder, bulamazsa Google araması hazırlar."""
    if "instagram" in komut: return "https://www.instagram.com", "Instagram"
    if "youtube" in komut: return "https://www.youtube.com", "YouTube"
    if "google" in komut: return "https://www.google.com", "Google"
    if "whatsapp" in komut: return "https://web.whatsapp.com", "WhatsApp"
    if "github" in komut: return "https://github.com", "GitHub"
    
    # Dinamik Arama İçin Kelime Temizliği
    silinecek_kelimeler = ["aç", "gir", "arat", "bul", "sitesine", "jarvis", "lütfen", "bana"]
    arama_terimi = komut
    for kelime in silinecek_kelimeler:
        arama_terimi = arama_terimi.replace(kelime, "")
        
    arama_terimi = arama_terimi.strip()
    
    if not arama_terimi:
        return "https://www.google.com", "Google"
        
    arama_linki = f"https://www.google.com/search?q={arama_terimi}"
    return arama_linki, f"'{arama_terimi}' araması"

def ana_dongu():
    konus("Sistem devrede. Arayüz başlatıldı.")
    while True:
        komut = dinle()
        if not komut:
            continue
            
        if "kapat" in komut or "çıkış yap" in komut:
            konus("Sistem kapatılıyor. İyi günler.")
            break
            
        elif "pdf oku" in komut:
            konus("PDF dosyası okunuyor.")
            icerik = pdf_oku("ornek.pdf")
            print(f"\n[PDF İÇERİĞİ]:\n{icerik}")
            konus("İçeriği terminale yazdırdım.")
            
        elif any(kelime in komut for kelime in ["aç", "gir", "arat", "bul"]):
            url, islem_adi = hedef_site_bul(komut)
            
            konus(f"{islem_adi} bilgisayarınızdan mı yoksa telefonunuzdan mı açılsın?")
            ikinci_komut = dinle() 
            
            if not ikinci_komut:
                konus("Cevap alamadım, işlemi iptal ediyorum.")
            elif "telefon" in ikinci_komut:
                konus("Şu anki sistemimizde telefona köprü kurmadığımız için bu işlemi yapamıyorum. Şimdilik iptal ettim.")
            elif "bilgisayar" in ikinci_komut:
                webbrowser.open(url) # Evrensel ve platform bağımsız tarayıcı açma komutu eklendi
                konus(f"{islem_adi} tarayıcı üzerinden başlatılıyor.")
            else:
                konus("Hangi cihazı istediğinizi net anlayamadım, işlemi iptal ettim.")
                
        else:
            cevap = yapay_zeka_yaniti(komut)
            print(f"Jarvis: {cevap}")
            konus(cevap)

# --- WEB ARAYÜZÜ ROTALARI ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    kullanici_mesaji = data.get("message")
    
    cevap = yapay_zeka_yaniti(kullanici_mesaji)
    konus(cevap)
    
    return jsonify({"reply": cevap})

if __name__ == "__main__":
    jarvis_thread = threading.Thread(target=ana_dongu)
    jarvis_thread.daemon = True
    jarvis_thread.start()
    
    webbrowser.open("http://localhost:5000")
    print("Arayüz otomatik olarak başlatıldı.")
    
    # Debug False ile Flask'ı başlatıyoruz
    app.run(host="0.0.0.0", port=5000, debug=False)