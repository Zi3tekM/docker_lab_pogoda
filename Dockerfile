# ETAP 1: Budowanie (Builder)
# Używamy lekkiej wersji Pythona na bazie Alpine Linux
FROM python:3.11-alpine AS builder

WORKDIR /app

# Kopiujemy listę bibliotek i instalujemy je w folderze lokalnym użytkownika
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ETAP 2: Obraz docelowy (Runtime) - to ten obraz zostanie wysłany na serwer
FROM python:3.11-alpine

# Metadane autora zgodnie ze standardem OCI
LABEL org.opencontainers.image.authors="Michal Zietek"

WORKDIR /app

# Kopiujemy tylko zainstalowane biblioteki z Etapu 1 (pomijamy zbędne pliki budowania)
COPY --from=builder /root/.local /root/.local
COPY app.py .

# Ustawiamy ścieżkę, aby Python widział skopiowane biblioteki
ENV PATH=/root/.local/bin:$PATH

# Healthcheck - sprawdza czy kontener żyje
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

# Informujemy, na którym porcie działa aplikacja
EXPOSE 5000

# Uruchomienie aplikacji
CMD ["python", "app.py"]