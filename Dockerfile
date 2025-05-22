FROM python:3.11-slim

# Gerekli linux paketlerini kur
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    gnupg \
    chromium-driver \
    chromium

# Ortam değişkenini ekle: chromedriver path Docker için
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]