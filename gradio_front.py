from http import server
import json
import gradio as gr
import requests
from fastapi import FastAPI

app_gradio = FastAPI()

pythonfastapi_url = "http://fast-api-service:80/predict"
url = "http://127.0.0.1:8000/predict"


def identify_whale(img):
    data = {"file": img}
    response = requests.post(pythonfastapi_url, data=json.dumps(data))
    return response.json()


iface = gr.Interface(
    fn=identify_whale,
    inputs=gr.Image(type='filepath'),
    outputs="text",
    title="Humpback Whale Identification",
    description="Upload an image of a whale to identify its ID."
)

# Запуск сервиса Gradio
#iface.launch(server_name = '0.0.0.0')
app_gradio = gr.mount_gradio_app(app_gradio, iface, path='/')