#
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

#
WORKDIR /code

ENV PYTHONUNBUFFERED=1 

# SYSTEM
RUN apt-get update --yes --quiet && DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    software-properties-common \
    build-essential apt-utils \
    wget curl vim git ca-certificates kmod \
    nvidia-driver-525 \
 && rm -rf /var/lib/apt/lists/*

# PYTHON 3.10
RUN add-apt-repository --yes ppa:deadsnakes/ppa && apt-get update --yes --quiet
RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3.10-lib2to3 \
    python3.10-gdbm \
    python3.10-tk \
    pip


#
RUN apt-get install -y ffmpeg && apt-get install -y apt-transport-https && apt-get install -y git

RUN pip install --upgrade pip

ENV PATH /home/${USER}/.local/bin:${PATH}

RUN pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118

RUN pip install onnxruntime

RUN pip install ffmpeg-python python-multipart==0.0.6 python-docx==0.8.11

RUN pip install huggingface-hub==0.15.1 transformers==4.31.0 pandas==1.5.3 uvicorn==0.22.0 fastapi==0.85.0 pydantic==1.10.8 

RUN pip install git+https://github.com/linto-ai/whisper-timestamped

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8500"]
