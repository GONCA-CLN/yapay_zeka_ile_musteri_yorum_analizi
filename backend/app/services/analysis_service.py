"""
Adımlar:
    1. Gerekli kütüphanelerin import edilmesi
    2. Yeni analiz oluşturur
    3. Geçmiş analizleri getirir

- bağımlılıkların yüklenmesi
        cd backend/
        fastapi requirements.txt ye yazılır
        pip install -r requirements.txt
"""

# ================================
# 1. Gerekli kütüphanelerin import edilmesi
# ================================

from sqlalchemy.ext.asyncio import AsyncSession # db de asyncsession nesnesi kurmak için
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.models.analysis import Analysis # ORM modeli (tablo)
from app.schemas.schemas import AnalysisResponse, AnalysisRequest, AnalysisListResponse
from app.services.gemini_service import analyze_sentiment

# ================================
# 2. Yeni analiz oluştur
# ================================

async def create_analysis(db: AsyncSession, payload: AnalysisRequest ) -> AnalysisResponse:
    try:
        gemini_result= await analyze_sentiment(payload.comment)
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_502_BAD_GATEWAY,
            detail = f"Gemini hatası: {str(e)}"
        )
    # sonuç başarılı gelirse ORM nesnesi hazırla
    analysis = Analysis(
        comment_text = payload.comment,
        sentiment = gemini_result["sentiment"],
        confidence = gemini_result["confidence"],
        explanation = gemini_result["explanation"]
    )

    # veri tabanına kaydet
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    return AnalysisResponse.model_validate(analysis)

# ================================
# 3. Geçmiş analizleri getir
# ================================

async def get_analyses(db: AsyncSession, skip: int=0, limit: int=50) -> AnalysisListResponse:

    # toplam kayıt sayısını al
    count_result = await db.execute(
        select(func.count()).select_from(Analysis)
    )
    total = count_result.scalar()

    # sayfalanmış kayıtları al
    rows= await db.execute(
        select(Analysis)
        .order_by(Analysis.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    analyses = rows.scalars().all()
    return AnalysisListResponse(
        total = total,
        analyses = [AnalysisResponse.model_validate(a) for a in analyses]
    )

