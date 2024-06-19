FROM python:3.10

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && mkdir /app

COPY requirements.txt /app

RUN pip install -r app/requirements.txt

COPY ./main.py /app
COPY ./input/* /app/input/
COPY ./model.keras /app

WORKDIR /app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
