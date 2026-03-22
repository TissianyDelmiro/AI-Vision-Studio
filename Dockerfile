FROM python:3.11-slim

# Instala dependências do sistema para OpenCV, MediaPipe e PyTorch
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos
COPY . .

# Instala as bibliotecas (pip upgrade ajuda a evitar erros de versão)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Porta do Hugging Face
EXPOSE 7860

# Comando para iniciar
CMD ["python", "app.py"]