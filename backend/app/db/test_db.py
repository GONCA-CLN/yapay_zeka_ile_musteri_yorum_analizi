"""
Adımlar: 
    1. gerekli kütüphanelerin import edilmesi
    2. test için doğrudan db bağlantısı kurmak
    3. tabloları oluşturmak
    4. test kaydı eklemek
    5. kaydı sorgulayıp ekrana yazdırmak
    6. test kaydını temizlemek

Not: 
    python -m app.db.test_db

"""
# ========================
# 1. gerekli kütüphanelerin import edilmesi
# ========================

import asyncio
from sqlalchemy import select

from app.models.analysis import Analysis
from app.db.database import AsyncSessionLocal, engine, init_db

# ========================
# 2&3 db ye bağlanma ve tabloları oluşturma 
# ========================

async def create_tables():
    """
    Amaç:
        database.py dosyasındaki init_db fonksiyonunu kullanarak 
        kendi engine'miz ile tabloları oluşturma
    """
    await init_db(engine_override=engine)
    print("Tablolar başarıyla oluşturuldu")

# ========================
# 4. test kaydı eklemek
# ========================

async def insert_test_record() -> int:
    """
    Amaç:
        analysis tablosuna sahte bir analiz kaydı ekleyip 
        veri tabanına yazma işlemini test etme    
    """
    async with AsyncSessionLocal() as db:
        analysis = Analysis(
            comment_text="Bu bir test yorumudur",
            sentiment="pozitif",
            confidence=0.99,
            explanation="Bu kayıt test_db.py tarafından oluşturuldu"
        )
        db.add(analysis)
        await db.commit()
        await db.refresh(analysis)

        print(f"test kaydı başarıyla eklendi: id={analysis.id}")

        return analysis.id

# ========================
# 5. kaydı sorgulayıp ekrana yazdırmak
# ========================
async def query_record(record_id:int):
    """
    Amaç:
        Az önce eklediğimiz kaydı id ile sorgulayıp ekrana yazdırmak
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Analysis).where(Analysis.id == record_id)
        )
        analysis=result.scalar_one_or_none()

    if analysis:
        print("\nSorgulanan Kayıt:")
        print(f"     id  :{analysis.id}")
        print(f"     comment_text  :{analysis.comment_text}")
        print(f"     sentiment  :{analysis.sentiment}")
        print(f"     explanation  :{analysis.explanation}")
    else:
        print("kayıt bulunamadı")

# ========================
# 6. test kaydını temizlemek
# ========================

async def delete_test_record(record_id: int):
    """
    Amaç:
        Test verisini silmek
    """

    async with AsyncSessionLocal() as db:

        result= await db.execute(
            select(Analysis).where(Analysis.id==record_id)
        )
        analysis=result.scalar_one_or_none()

        if analysis:
            await db.delete(analysis)
            await db.commit()

        print(f"test kaydı başarıyla silindi. id={record_id}")


# ========================
# 7. Standalone testleri
# ========================

async def _main():
    print("="*50)
    print("veritabanı test işlemleri başladı")
    print("="*50)

    await create_tables()

    record_id = await insert_test_record()

    await query_record(record_id)
    await delete_test_record(record_id)

    print("Tüm testler başarılı bir şekilde tamamlandı")

    await engine.dispose()

if __name__=="__main__":
    asyncio.run(_main())
