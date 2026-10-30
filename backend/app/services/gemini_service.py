r"""
ADIMLAR:
    1. gerekli kütüphanelerin import edilmesi
    2. API key ile gemini client oluşturma
    3. ilk basit mesajlaşma yapılacak
    4. Duygu analizi için promt hazırlamak
    5. Bir metin üzerinde async duygu analizi yapmak
    6. sonucu json olarak döndürmek 

kurulum:
    - venv oluşturma: python -m venv venv 
    - venv aktif etme: .\venv\Scripts\activate
    - requirements.txt dosyasına 
        google-genai
        python-dotenv
    - bağımlılıkların yüklenmesi
        cd backend/
        pip install -r requirements.txt
    - backend/.env dosyasına API key in yazılması
        GEMIN_API_KEY= google genai studio dan alınan key

"""

# ========================
# 1. Gerekli kütüphanelerin import edilmesi
# ========================

import asyncio
import json
import os
import sys

from google import genai
from dotenv import load_dotenv

# .env dosyasının yüklenmesi
load_dotenv()

# ========================
# 2. API key ile gemini client oluşturma
# ========================

# API key ortam değişkeninden yüklenecek (.env dosyasından)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError("GEMIN_API_KEY bulunamadı, lütfen .env dosyasını kontrol ediniz")

# model seçimi
MODEL_NAME = "gemini-3.8-flash"


# Gemini Client oluştur
Client=genai.Client(api_key=GEMINI_API_KEY)

# ========================
# 3. ilk basit mesajlaşma yapılacak
# ========================

async def first_message():
    """
    Amaç:
        Gemini API bağlantısının test edilmesi ve basit mesaşlaşmanın yapılmas
    """
    response = await Client.aio.models.generate_content(
        model=MODEL_NAME,
        contents="merhaba gemini, bana kısa bir selam ver"

    )

    print("ilk gemini çağrısı:")

    # Gelen cevap parçacıklarını (chunk) anlık olarak ekrana basıyoruz
    # async for chunk in response:
    #     print(chunk.text, end="", flush=True)

    print(response.text)
    print()

# ========================
# 4. Duygu analizi için promt hazırlamak
# ========================
def build_sentiment_promt(comment: str) -> str:
    """
    Amaç:
        yapay zeka modeline verilecek yorumun duygu analizni yapması için açık ve yapılandırılmış bir promt hazırlamak
    """
    promt=f"""
    Sen bir duygu analizi uzmanısın. Sana verilen müşteri yorumunu analiz et ve aşağıdaki JSON formatında yanıt ver. JSON dışında hiç bir şey yazma.

    Yorum: "{comment}"

    Yanıt formatı: 
    {{
        "sentiment": "pozitif" | "negatif" | "nötr"
        "confidence" 0.0 ile 1.0 arasında bir sayı.
        "explanation": "kısa Türkçe açıklama (maksimum 2 cümle)"
    }}
    """
    return promt.strip()

# ========================
# 5. Bir metin üzerinde async duygu analizi yapmak
# ========================

async def analyze_sentiment(comment: str) -> dict:
    """
    Amaç:
        verilen yorumu gemini ile async olarak analiz etmek

    Args:
        comment: Analiz edilecek yorum
    
    returns:
        sentiment, confidence, explanation anahtarlarını içeren bir dict

    raise: 
        ValueError: Gemini geçerli bir JSON dönmezse
    """
    promt = build_sentiment_promt(comment)

    # Gemini ye client ile istek atmak
    response = await Client.aio.models.generate_content(
        model=MODEL_NAME,
        contents=promt   
        )
    
    raw_text=response.text.strip()

    # JSON parse işlemleri

    # gemini bazen cevabı ''' JSON ... bloğu içerisinde sarabilir. buunların temizlenmesi lazım

    if raw_text.startswith("'''"):
        raw_text = raw_text.split("'''")[1]

        if raw_text.startswith("json"):
            raw_text = raw_text.split[4:]

    try:
        result= json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini geçersiz bir JSON döndürdü: {raw_text}") from e

    # beklenen key lerin cevabın içerisinde olduğunu doğrulayalım
    required_keys= {"sentiment", "confidence", "explanation"}

    if not required_keys.issubset(result.keys()):
        raise ValueError(f"Gemini yanıtında eksiklikler var {result}")
    
    return result



# ========================
# Standalone test: Bu dosya doğrudan çalıştırılırsa yapacağı işlemler
# ========================

async def _main():

    # adım 3 ü gerçekleştir
    # await first_message()
    # print(build_sentiment_promt("Naber?"))

    # adım 5 ve 6 yı test et
    if len(sys.argv)>1:
        comment = " ".join(sys.argv[1:])
    else:
        comment = input("Analiz edilecek yorum: ").strip()
        if not comment:
            print("Hata: yorum boş olamaz")
            sys.exit(1)
    
    print(f"\nYorum: {comment}")
    print("Gemini analiz ediyor...\n")

    Result = await analyze_sentiment(comment)

    print(f"Duygu   : {Result['sentiment']}")
    print(f"Güven   : %{int(Result['confidence'] * 100)}")
    print(f"Açıklama   : {Result['explanation']}")
   

if __name__=="__main__":
    # async bir fonksiyon çalıştırılacağı için async.run metodu kullanılacak
    asyncio.run(_main())