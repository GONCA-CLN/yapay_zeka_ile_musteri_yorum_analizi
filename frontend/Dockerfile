# ======================
# 1. Adım Base Image seçmek
# ======================

FROM python:3.11-slim

# ======================
# 2. Çalışma dizinini ayarlamak
# ======================

WORKDIR /app

# ======================
# 3. Bağımlılıkların yüklenmesi
# ======================

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ======================
# 4. Uygulamanın kodunu kopyalamak
# ======================

COPY . .

# ======================
# 5. Portu dışarı aç
# ======================

EXPOSE 8501

# ======================
# 6. Başlatma komutu tanımla
# ======================

CMD ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--browser.gatherUsageStats=false", \
    "--server.headless=true"]