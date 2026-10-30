"""
Adımlar:
    1. gerekli kütüphanelerin import edilmesi
    2. Settings sınıfının (class) oluşturulması ve BaseSettings üzerinden türetilmesi
    3. DATABASE_URL ve GEMINI_API_KEY'in tanımlanması
    4. async_database_url özelliğinin eklenmesi ve DATABASE_URL ortam değişkeninin asyncpg formatına getirilmesi
    5. settings örneğini oluşturmak

Kurulum:
    1. pydantic-settings kütüphanesinin requirements.txt dosyasına eklenmesi
        pydantic-settings
    2. Bağımlılıkların yüklenmesi
        pip install -r requirements.txt
    3. .env dosyasına gerekli ortam değişkeninin eklenmesi
        DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/yorum_analizi 
            (postgres:postgres - yükleme esnasında default gelen "kullanıcı adı: şifre" )  
            (yorum_analizi: kullanılacak db adı)
"""

# ==========================
# 1. gerekli kütüphanelerin import edilmesi
# ==========================

from pydantic_settings import BaseSettings
from typing import List

# ==========================
# 2. Settings sınıfının (class) oluşturulması ve BaseSettings üzerinden türetilmesi
# ==========================

class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str
    ALLOWED_ORIGINS: str = "http://localhost:8501"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()] # birden fazla ALLOWED_ORIGINS varsa bunları virgülle ayır ve geri döndür


    @property
    def async_database_url(self) -> str:
        url = self.DATABASE_URL

        if url.startswith("postgresql://"):
            url=url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgres://"):
            url=url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()