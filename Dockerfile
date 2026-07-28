FROM python:3.9-slim

# Instalar el motor de IA Tesseract y librerias de sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar librerias de Python
RUN pip install pytesseract watchdog Pillow

# Crear directorio de trabajo
WORKDIR /app

# Copiar el script
COPY organizador.py .

# Ejecutar el script
CMD ["python", "-u", "organizador.py"]