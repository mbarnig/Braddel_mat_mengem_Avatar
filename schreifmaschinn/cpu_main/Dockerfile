#
FROM python:3.10

#
WORKDIR /code

#
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg && apt-get install -y apt-transport-https && apt-get install -y git

RUN pip install --upgrade pip

ENV PATH /home/${USER}/.local/bin:${PATH}

RUN pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1

RUN pip install ffmpeg-python python-multipart==0.0.6 python-docx==0.8.11

RUN pip install huggingface-hub==0.15.1 transformers==4.31.0 pandas==1.5.3 uvicorn==0.22.0 fastapi==0.85.0 pydantic==1.10.8 

RUN pip install git+https://github.com/linto-ai/whisper-timestamped

#RUN ["chmod", "+x", "/code/startup_script.sh"] 

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8500"]
