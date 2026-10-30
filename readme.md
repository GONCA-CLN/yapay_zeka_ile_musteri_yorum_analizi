# Yapay zeka ile müsteri yorum analizi

Gemini, PostgreSQL, FastAPI, Docker ve Railway uçtan uca bir duygu analizi projesi

# Proje Akışı

Gemini --> PostgreSQL -->  FastAPI -->  Docker -->  Railway


# Adım 1: Gemini ile yorum analizi ve iyileştirme önerileri geliştirme

**ne yapacağız?**

Google Gemini yapay zeka modeline API ile bağlanıp müsteri yorumlarını duygu analizine göre sınıflandıracağız

**Dosya** "backend/app/services/gemini_service.py" 

**Neler öğreneceğiz**

- "google-genai" SDK kurulumunu ve virtual environment kullanımını öğreneceğiz
- "genai.client" ile API bağlantısı kurulması
- promt ile yapay zeka modeline ne dememiz gerektiğini öğreneceğiz
- json formatında yapılandırılmış yanıt almayı ve bunu kullanmayı
- asenkron gemini çağrısını görmüş olacağız

Google Gemini API key
- AQ.Ab8RN6IjQRGc22N9sefqrL8A1jJBHVe_bVp_pN5jt__aKe8Zew

# Adım 2: PostgreSQL ile analiz sonuçlarını kaydetme

**ne yapacağız?**
her analiz sonucunu veri tabanına kaydedecek ve böylece geçmiş analizlere erişecek ve istatistikler gösterebileceğiz

**önce PostgreSQL kur: https://www.postgresql.org/download/windows/ (yükleme adımında LOCAL:English olsun)**
**-server in altında veri ilk dizinin adı "postgres" olacak**

**Dosya** 
- "backend/app/core/config.py" ortam değişkenlerin temel yapılandırmaları ve uygulama genel ayarlarını yöneteceğimiz merkezi dosya
- "backend/app/db/database.py" async engine ulaşmak, session almak, db ye ulaşmak için
- "backend/app/models/analysis.py" analysis tablosu ORM modeli

**Neler öğreneceğiz**
- Pydantic setting ile ".env" dosyasından config okuma
- SQLALchemy async engine kurulumu
- ORM model tanımlama (Python class - veritabanı tablosu)
- async session yönetimi ve "get_db" dependency pattern'i

# Adım 3: FastAPI ile Yorum Analizi API'si geliştirme 

**ne yapacağız?**
Gemini (Adım 1) ve PostgreSQL (Adım2) servislerini bir REST API servisine bağlayacağız
iki adet endpoint tasarlanacak
    - "POST /api/v1/analysis" -> yorum gönder, analiz sonucunu al ve kaydet
    - "GET /api/v1/analysis/history" -> geçmiş analizleri listele

**Dosya** 

- "backend/main.py" uygulamanın giriş noktası, CORS, lifespan
- "backend/app/schemas/schemas.py" request/response şemaları - veri yapısı standartlaştırma
    (hatalı veri alımı ve gönderimini önlemek için - kod daha güvenli ve okunur hale geliyor)
- "backend/app/api/routes/analysis.py" -> endpoint tanımları
- "backend/app/services/analysis_service.py" -> Gemini + PostgreSQL iş mantığı

**Neler öğreneceğiz**

- fastapi kurulumu ve async uygulama oluşturma
- Pydantic ile otomatik veri doğrulama (schemas)
- CORS middleware (Streamlit'in API ye erişebilmesi için)
- lifespan ile async tablo oluşturma
- Dependency injection ile "get_db" kullanımı
- swagger UI ile otomatik dökümantasyon ("/docs")

# Adım 4: Streamlit ile Kullanıcı Arayüzü Geliştirme

**ne yapacağız?**

Kullanıcıların yorum yazabileceği ve geçmiş yorumları görüntüleyebileceği bir arayüz geliştirilecek

**Dosya** 
"frontend/app.py" - tek bir sayfada ayarlar, dashbord form ve geçmiş yer alacak
"frontend/api_client.py" - FastAPI ye request kütüphanesi ile HTTP istekleri gönderecek 


**Neler öğreneceğiz**

- Streamlit kurulumu ve "streamlit run" komutu ile bir streamlit app çalıştırma
- "session_state" ile sayfa yenilendiği zaman veriyi koruma
- "requests" kütüphanesiyle FastAPI ye istek atma öğrenilecek


# Adım 5: Docker ile paketleme

**ne yapacağız?**

Tüm servisler docker container'a paketlenecek ve tek komutla hespsi ayağa kaldırılacak

**Dosya** 

-"backend/Dockerfile" - Backend'i image olarak paketleyecek
-"frontend/Dockerfile" - Frontend'i image olarak paketleyecek
-"docker-compose.yml" - Servisleri birleştirerek çalıştırmamızı sağlar

Çalıştımak için
    - Docker uygulamasını çalıştır
    - docker compose up --build

**Neler öğreneceğiz**

-"Dockerfile" yazımı
-"docker-cpmpose.yml" ile birden fazla servisi bir yapı halinde kullanma
-"healthcheck" ve "depends_on" kullanarak servislerin başlangıç sıralamasını yapma

# Adım 6: Deploy

**ne yapacağız?**

Uygulama Railway üzerinden deploy edilecek
    Backend (FastAPI), frontend(Streamlit) ve Database (PostgreSQL) ayrı ayrı ayağa kaldırılıp deploy edilecek

**Dosya** 



**Neler öğreneceğiz**

- Railway üzerinde mono repo yapısıyla çoklu servisleri deploy etmeyi
    backend ve frontend github da tek bir repo içerisinde olacak şekilde deploy edilecek
- Root directory ile farklı klasörleri ayrı servislere bağlama (Railway özelliği)
- Managed_PostgreSQL ve servisler arası reference kullanımı
    ortam değişkenlerini değiştirerek postgresql'i birbirine bağlayacağız

**Ön Koşullar**,

- Github hesabı ve projeyi barındıran bir repo

    projeyi repoya push etme:

    git init
    git add .
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/GONCA-CLN/yapay_zeka_ile_musteri_yorum_analizi.git
    git push -u origin main


- Railway hesabı






