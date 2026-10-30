"""
Adımlar:
    - AnalysisRequest modelini tanımla (istemciden gelen)
    - AnalysisResponse modelini tanımla (istemciye dönen veri)
    - AnalysisListResponse modelini tanımla (geçmiş verileri listelemel için)
NOT:
    Pydantic modeli iki işe yarar
        - Gelen veriyi otomatik doğrular (tip, zorunlu alan, vb)
        - Giden veriyi JSON a dönüştürür
    FastAPI bu modelleri Swagger UI da da otomatik belgeler

"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    """
    POST /analysis/ endpointine gelecek JSON gövdesi
    """
    comment: str

class AnalysisResponse(BaseModel):
    """
    Analiz tamamlandığında döndürülen JSON yanıtı.
    
    from_attributes=True: SQLAlchemy ORM nesnesini doğrudan bu modele dönüştürülmesini sağlar
    """
    id: int
    comment_text: str
    sentiment: str
    confidence: float
    explanation: Optional[str] # opsiyonel her zaman kaydetmemiz gerekmiyor
    created_at: datetime

    class Config:
        from_attributes=True

class AnalysisListResponse(BaseModel):
    """
    GET /analysis/history endpointinin döndürdüğü yanıt
    """
    total: int # veri tabanındaki toplam veri sayısı
    analyses: list[AnalysisResponse]
