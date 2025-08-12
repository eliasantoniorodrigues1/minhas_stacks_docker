# Usa uma imagem base do Python 3.10
FROM python:3.10

# Define um diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y git libsndfile1

# Clona o repositório do Bark
RUN git clone https://github.com/suno-ai/bark.git .

# Copia o arquivo server.py para o container
COPY server.py /app/server.py

# --- Alteração crucial ---
# 1. Instala as dependências do PyTorch de forma separada, usando o índice de URLs específico.
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 2. Instala as dependências gerais do projeto, como Flask e scipy, do repositório padrão.
RUN pip install Flask scipy

# Instala as demais dependências do Bark.
RUN pip install .

# Adiciona a variável de ambiente para resolver o erro de pickle
ENV BARK_INSECURE_PYTORCH_PICKLE=1

# Expõe a porta 5000, a porta padrão do Flask
EXPOSE 5000

# Define o comando padrão para iniciar o servidor web que criamos
CMD ["python", "server.py"]