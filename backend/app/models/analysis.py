"""
Adımlar:
    1. gerekli kütüphanelerin import edilmesi
    2. Base den miras alarak ORM modelinin tanımlanması
    3. tablo adının belirlenmesi
    4. kolonları ve tipleri tanımlamak
"""

# ======================
# 1. gerekli kütüphanelerin import edilmesi
# ======================

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func
from app.db.database import Base


# ======================
# 2. Base den miras alarak ORM modelinin tanımlanması
# ======================

class Analysis(Base):
    
    # ======================
    # 3. tablo adının belirlenmesi
    # ======================

    __tablename__="analysis"

    # ======================
    # 4. kolonları ve tipleri tanımlamak
    # ======================

    id = Column(Integer, primary_key=True, index=True)
    comment_text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
        )



