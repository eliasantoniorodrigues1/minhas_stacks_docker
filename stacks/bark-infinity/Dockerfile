FROM nvidia/cuda:11.8.0-base-ubuntu22.04 as cuda

ENV PYTHON_VERSION=3.10

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    libsndfile1-dev \
    git \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python3 && \
    ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

RUN pip install --upgrade pip

RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

FROM cuda as app
# 1. Copia os arquivos da aplicação para o container
COPY . /src

WORKDIR /src

# 2. Instalar dependências de sistema para compilação
# 'build-essential' inclui o g++ e outras ferramentas de compilação C/C++
# 'libsndfile1' e 'libsox-dev' são dependências comuns para pacotes de áudio como fairseq
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
    libsox-dev && \
    rm -rf /var/lib/apt/lists/*

# 3. Downgrade do pip para uma versão compatível (anterior à 24.1)
# Isso resolve o problema de metadados com omegaconf
RUN pip install "pip<24.1"

# 4. Instalação das dependências do requirements-pip.txt
RUN pip install -r requirements-pip.txt

# 5. Instalação de pacotes adicionais necessários
RUN pip install encodec rich-argparse

EXPOSE 8082
CMD ["python", "bark_webui.py"]