FROM python:3.8.4-slim-buster
#FROM tensorflow/tensorflow:latest-devel-gpu-py3
COPY . usr/src/app
WORKDIR /usr/src/app
#WORKDIR /app

#COPY requirements.txt .
#COPY . .
#RUN apt update
#RUN apt install --yes build-essential libhdf5-dev 
#RUN apt install libhdf5-dev
#RUN pip install -r requirements.txt
RUN pip install --no-cache-dir \
        tensorflow-cpu \
        pandas \
        numpy \
        requests \
        keras \
        fastapi \
        uvicorn
RUN pip install --upgrade fastapi pydantic typing-extensions

ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload