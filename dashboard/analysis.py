import glob

import numpy as np
import streamlit as st
import tensorflow as tf

from .media import make_gradcam_heatmap, overlay_heatmap_on_image, preprocess_image
from .settings import LAST_CONV_LAYER_NAME, MAX_DISPLAY_CONFIDENCE, MODEL_PATH, TRAINING_DIR


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(str(MODEL_PATH))


@st.cache_data
def get_example_images():
    madura = sorted(
        glob.glob(str(TRAINING_DIR / "dataset" / "test" / "madura" / "*"))
    )
    nao_madura = sorted(
        glob.glob(str(TRAINING_DIR / "dataset" / "test" / "nao_madura" / "*"))
    )

    examples = {}
    if madura:
        examples["Exemplo madura"] = madura[0]
    if nao_madura:
        examples["Exemplo não madura"] = nao_madura[0]

    return examples


def limit_display_confidence(confidence):
    return min(float(confidence), MAX_DISPLAY_CONFIDENCE)


def get_result_style(confidence):
    if confidence >= 0.90:
        return {
            "bg": "#F7F1E8",
            "border": "#30391F",
            "title": "Alta confiança",
            "text": "O modelo identificou o resultado com alta segurança."
        }
    if confidence >= 0.70:
        return {
            "bg": "#FFF7E8",
            "border": "#B58A4A",
            "title": "Confiança moderada",
            "text": "O modelo encontrou um resultado plausível, mas com segurança intermediária."
        }
    return {
        "bg": "#FFF0F4",
        "border": "#C00646",
        "title": "Baixa confiança",
        "text": "O modelo encontrou um resultado incerto. Vale a pena testar outra imagem."
    }


def get_prediction_text(predicted_class, confidence):
    display_confidence = limit_display_confidence(confidence)
    if predicted_class == "madura":
        return f"A IA identificou que a lichia está madura com confiança de {display_confidence:.2%}."
    return f"A IA identificou que a lichia está não madura com confiança de {display_confidence:.2%}."


def analyze_image(image, image_source_name, model):
    processed_image, image_array = preprocess_image(image)

    prediction = model.predict(image_array, verbose=0)[0][0]

    if prediction >= 0.5:
        predicted_class = "não madura"
        confidence = prediction
    else:
        predicted_class = "madura"
        confidence = 1 - prediction

    heatmap = make_gradcam_heatmap(image_array, model, LAST_CONV_LAYER_NAME)
    heatmap_image = overlay_heatmap_on_image(processed_image, heatmap)

    return {
        "file_name": image_source_name,
        "processed_image": processed_image,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "display_confidence": limit_display_confidence(confidence),
        "heatmap_image": heatmap_image,
        "style": get_result_style(confidence),
        "prediction_text": get_prediction_text(predicted_class, confidence)
    }
