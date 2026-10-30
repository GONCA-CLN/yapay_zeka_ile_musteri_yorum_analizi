"""
Adımlar:
    1. Gerekli kütüphanelerin import edilmesi ve API_BASE_URL ortam değişkenini okuma
    2. Yorum analizi isteği at
    3. Analiz geçmişini getir

Kurulum:
    1. requirements.txt dosyasına gerekli kütüphaneleri ekle
        streamlit
        requests
        python-dotenv
    2. bağımlılıkların yükle
        pip install -r requirements.txt
    3. frontend/.env dosyasına API_BASE_URL ortam değişkenini ekle
        Local geliştirmede: http://localhost:8000/api/v1 
"""

# =========================
# 1. Gerekli kütüphanelerin import edilmesi ve API_BASE_URL ortam değişkenini okuma
# =========================

import requests
import os

from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()
API_BASE_URL=os.getenv("API_BASE_URL")


# =========================
# 2. Yorum analizi isteği at
# =========================

def analyze_comment(comment:str) -> dict:
    """
    Amaç:
        kullanıcının yazdığı yorumu FastAPI ye gönderip Gemini analiz sonucunu döndürmek
    """
    response = requests.post(
        f"{API_BASE_URL}/analysis/",
        json={"comment": comment}
        # timeout=30 # gemini bazen geç cevap verebilir
    )

    response.raise_for_status()
    return response.json()

# =========================
# 3. Analiz geçmişini getir
# =========================

def get_history(skip: int=0, limit: int=50) -> dict:
    """
    Amaç:
        Veritabanından geçmiş analizleri getirmek
    """
    response = requests.get(
        f"{API_BASE_URL}/analysis/history",
        params={"skip":skip, "limit": limit},
        timeout=10
    )

    response.raise_for_status()
    return response.json()
