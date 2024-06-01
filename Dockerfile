FROM mirror.gcr.io/python:3.9.5

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y \
    && mkdir /app


COPY ./config/* ./app/config/
COPY ./trainer/* ./app/trainer/
COPY ./app.py/ ./app

WORKDIR /app

RUN cd config && pip install -r requirements.txt

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

VOLUME ./app/config

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
