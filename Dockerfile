FROM python:3.11-slim

# Instala as ferramentas de vídeo que o Linux precisa
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos do seu PC
COPY . .

# Instala as bibliotecas do seu requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Porta padrão do Hugging Face
EXPOSE 7860

# Comando para ligar o site
CMD ["python", "app.py"]