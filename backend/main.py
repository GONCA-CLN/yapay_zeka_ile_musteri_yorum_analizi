"""
Adımlar:
    1. Gerekli kütüphanelerin import edilmesi
    2. lifespan tanımlamak (uygulamanın açılıp kapanırken ne yapacağını belirlemek)
    3. FastAPI uygulamasının oluşturulması
    4. CORS middleware in eklenmesi
    5. Router'ları uygulamaya kaydetmek
    6. Health Check endpointinin yazılması
    7. Çalıştırmak için: 
        cd backend
        uvicorn main:app --reload

Kurulum:
    1. requirements.txt dosyasına gerekli kütüphanelerin eklenmesi
        fastapi
        uvicorn[standart]
    2. Bağımlılıkların yüklenmesi
        cd backend
        pip install -r requirements.txt
    3. Uygulamayı başlatmak
    4. Swagger üzerinden testler

"""
# ================================
# 1. Gerekli kütüphanelerin import edilmesi
# ================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analysis
from app.core.config import settings
from app.db.database import engine, Base, init_db


# ================================
# 2. lifespan tanımlamak (uygulamanın açılıp kapanırken ne yapacağını belirlemek)
# ================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Uygulama başlarken eğer tablolar (db tabloları) oluşmadıysa bunları oluştur
    """
    await init_db(engine_override=engine)
    yield

    await engine.dispose()

# ================================
# 3. FastAPI uygulamasının oluşturulması
# ================================

app=FastAPI(
    title="Yapay Zeka ile Müşteri Yorum Analizi",
    description="Gemini Kullanarak Müşteri Yorum Analizi",
    version="1.0.0",
    lifespan=lifespan
)

# allowed_origins_list'i config settings'den al (izin verilen kaynakları alıyor)

# ================================
# 4. CORS middleware in eklenmesi
# ================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"], # bütün metotları kabul et
    allow_headers=["*"] # bütün header'ları kabul et
)

# ================================
# 5. Router'ları uygulamaya kaydetmek
# ================================

app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analizler"])

# ================================
# 6. Health Check endpointinin yazılması
# ================================
@app.get("/", tags=["Health"])
async def health_check():
    return{
        "status": "ok",
        "message": "Yapay Zeka ile Müşteri Yorum Analizi Çalışıyor"
    }