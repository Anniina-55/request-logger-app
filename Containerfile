FROM docker.io/library/python:3.11-slim

WORKDIR /app

# Kopioi riippuvuudet
COPY requirements.txt .

# asenna Flask
RUN pip install --no-cache-dir -r requirements.txt

# kopioi lähdekoodi
COPY . .

# API portti
EXPOSE 5000

# käynnistyskomento
CMD ["python", "app.py"]
