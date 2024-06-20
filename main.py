from fastapi import FastAPI, File, UploadFile
from typing import Annotated

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder
import cv2

app = FastAPI()

@keras.utils.register_keras_serializable()
class NGL(tf.keras.losses.Loss):
    def __init__(
    	self,
    	scaling=False,
    	name="ngl_loss",
        reduction=tf.keras.losses.Reduction.AUTO,):
        super().__init__(name=name)
        self.name = name
        self.scaling = scaling

    def call(self, y_true, y_pred):
        y_true = tf.cast(y_true, tf.float32)
        y_pred = tf.cast(y_pred, tf.float32)
        if self.scaling == True:
	 	        y_pred = tf.math.sigmoid(y_pred)
        part_1 = tf.math.exp(2.4092 - y_pred - y_pred*y_true)
        part_2 = tf.math.cos(tf.math.cos(tf.math.sin(y_pred)))
        elements = part_1 - part_2
        loss = tf.reduce_mean(elements)
        return loss


custom_objects = {"NGL": NGL}
with tf.device('/cpu:0'):
    with keras.utils.custom_object_scope(custom_objects):
        reconstructed_model = keras.models.load_model("model.keras")



data = pd.read_csv("input/train.csv")
filtered_data = data['Id']
# Создание объекта LabelEncoder
label_encoder = LabelEncoder()

# Преобразование строковых идентификаторов классов в числовые метки
classes_id = label_encoder.fit_transform(data["Id"])

# Создание словаря для соответствия числовых меток и строковых идентификаторов
class_dict = {class_id: class_name for class_id, class_name in zip(classes_id, data["Id"])}


# Функция для идентификации кита по загруженному изображению
def identify_whale(img):
    # with open(img, 'rb', encoding='utf-8') as f:
    #     imgg = f.read()
    # decoded = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
    # pg_image = cv2.resize(decoded, (220, 220))
    x = image.load_img(img, target_size=(224, 224))
    x = image.img_to_array(x)
    x = tf.image.resize(x, [100, 100])
    x = x / 225

    x = np.expand_dims(x, axis=0)

    prediction = reconstructed_model.predict(x, verbose=0)
    whale_id = np.argmax(prediction)

    class_name = class_dict[whale_id]

    return class_name



@app.get("/readiness")
async def root():
    return {"message": "Service is ready"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/predict")
async def predict(data: dict):
    filepath = data.get("file")
    class_name = identify_whale(filepath)
    return class_name


