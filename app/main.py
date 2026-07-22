
import streamlit as st
import tensorflow as tf
from keras.layers import TFSMLayer
from keras import Sequential
from PIL import Image
import numpy as np
import os

# Load SavedModel

working_dir = os.path.dirname(os.path.abspath(__file__))

saved_model_path = os.path.join(
    working_dir,
    "trained_model",
    "fashion_savedmodel"
)

# Wrap SavedModel as a Keras model
model = Sequential([
    TFSMLayer(saved_model_path, call_endpoint="serve")
])


# Class labels

class_names = [
    'T-shirt/top',
    'Trouser',
    'Pullover',
    'Dress',
    'Coat',
    'Sandal',
    'Shirt',
    'Sneaker',
    'Bag',
    'Ankle boot'
]


# Image preprocessing

def preprocess_image(uploaded_file):
    img = Image.open(uploaded_file)

    img = img.convert("L")          # grayscale
    img = img.resize((28, 28))

    img = np.array(img).astype("float32") / 255.0
    img = img.reshape(1, 28, 28, 1)

    return img


# Streamlit UI

st.title("Fashion Item Classifier")

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:

    image = Image.open(uploaded_image)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, width=200)

    with col2:

        if st.button("Classify"):

            img = preprocess_image(uploaded_image)

            predictions = model(img)

            predictions = np.array(predictions)

            predicted_class = np.argmax(predictions)

            st.success(
                f"Prediction : {class_names[predicted_class]}"
            )