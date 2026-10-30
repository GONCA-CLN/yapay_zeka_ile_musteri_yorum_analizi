"""
Adımlar:
    1. Gerekli kütüpanelerin import edilmesi
    2. Async SQLAlchemy engine oluşturmak
    3. Async session factory oluşturmak
    4. Base class oluşturmak
    5. get_db dependency oluşturmak

kurulum:
    1. gerekli kütüphanelerin reğuirements.txt ye eklenmesi
        sqlalchemy[asyncio]
        asyncpg
    2. bu bağımlılıkların yüklenmesi
        pip install -r requirements.txt

"""

# =============================
# 1. Gerekli kütüpanelerin import edilmesi
# =============================

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# =============================
# 2. Async SQLAlchemy engine oluşturmak
# =============================

engine = create_async_engine(
    settings.async_database_url,
    pool_size=5, # aynı anda kaç tane bağlantı açık kalacak
    max_overflow=10, # pool_size ın tamamı doluysa ekstra kaç bağlantı açılabilecek 
    echo=False # SQL sorgularının terminale yazılıp yazılmayacağı
)

# =============================
# 3. Async session factory oluşturmak
# =============================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

# =============================
# 4. Base class oluşturmak
# =============================

Base = declarative_base()

# =============================
# 5. get_db dependency oluşturmak
# =============================

async def init_db(engine_override=None):
    """
    Veri tabanında tabloları oluşturur
    uygulama başlarken çağırılır, 
    henüz db ve tablolar oluşturulmadıysa db ve tablolar oluşturulur
    """
    use_engine = engine_override or engine
    async with use_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """
    Amaç: 
        fastAPI endpointlerine async veri tabanı session'ı sağlamak

    Nasıl çalışır:
        async with ile session açılır > endpointe verilir > blok bitince otomatik kapatılacak
    
    Kullanım:
        async def analyze(db: AsyncSession = Depend(get_db))
    """

    async with AsyncSessionLocal() as session:
        yield session