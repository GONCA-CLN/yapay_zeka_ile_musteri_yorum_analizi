"""
Adımlar:
    1. Gerekli kütüphanelerin yüklenmesi ve Router'in oluşturulması
    2. POST / -> endpointinin yazılması
    3. GET /history -> endpointinin yazılması
"""

# ======================
# 1. Gerekli kütüphanelerin yüklenmesi
# ======================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.schemas import AnalysisResponse, AnalysisRequest, AnalysisListResponse
from app.services import analysis_service

# Router oluştur
router = APIRouter()

# ======================
# 2. POST / -> endpointinin yazılması
# ======================

@router.post("/", response_model=AnalysisResponse, status_code=201)
async def analyze(
    payload: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
):
    return await analysis_service.create_analysis(db, payload)

# ======================
# 3. GET /history -> endpointinin yazılması
# ======================

@router.get("/history", response_model=AnalysisListResponse)
async def get_history(
    skip: int = Query(default=0, ge=0, description="Atlanacak kayıt sayısı"),
    limit: int =  Query(default=50, ge=1, le=100, description="Döndürülecek maksimum ve minimum kayıt sayısı"),
    db: AsyncSession = Depends(get_db)
):
    return await analysis_service.get_analyses(db, skip, limit)
    
