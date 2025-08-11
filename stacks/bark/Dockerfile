# Dockerfile para Bark TTS (local build)
FROM python:3.10-slim

# Atualiza e instala dependências básicas
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Configura o diretório de trabalho
WORKDIR /app

# Copia requirements.txt com as libs do Bark
RUN pip install --upgrade pip

# Instala as dependências do Bark
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
RUN pip install flask flask-cors transformers scipy numpy soundfile

# Clona o repositório Bark do GitHub
RUN git clone https://github.com/suno-ai/bark.git .

# Copia o server.py para o diretório de trabalho
COPY docker/stacks/bark/server.py /app/
# Expõe a porta que o Bark usa
EXPOSE 5000

# Define variável de ambiente para usar GPU (ajuste conforme sua configuração)
ENV BARK_USE_GPU=true

# Comando para rodar o servidor Bark
CMD ["python3", "server.py"]
