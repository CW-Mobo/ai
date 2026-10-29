import base64
import io

import matplotlib
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from .settings import CSS_PATH, IMG_HEIGHT, IMG_WIDTH


def load_css():
    if CSS_PATH.exists():
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def image_to_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception:
        return ""


def pil_image_to_data_uri(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def preprocess_image(image):
    image = image.convert("RGB")
    image_resized = image.resize((IMG_WIDTH, IMG_HEIGHT))
    image_array = np.array(image_resized, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_resized, image_array


def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    base_model = model.get_layer("mobilenetv2_1.00_224")

    # Cria modelo funcional passando pelo base_model e depois pelas camadas restantes
    inputs = tf.keras.Input(shape=img_array.shape[1:])
    conv_outputs = base_model(inputs)
    
    # Pega saída da última conv dentro do base_model
    inner_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=base_model.get_layer(last_conv_layer_name).output
    )

    with tf.GradientTape() as tape:
        conv_out = inner_model(img_array)
        tape.watch(conv_out)
        
        # Passa conv_out pelo resto do modelo manualmente
        x = conv_out
        for layer in model.layers[1:]:  # pula o base_model
            x = layer(x)
        predictions = x
        class_channel = predictions[:, 0]

    grads = tape.gradient(class_channel, conv_out)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    heatmap = conv_out[0] @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    max_val = tf.math.reduce_max(heatmap)
    if max_val == 0:
        return np.zeros_like(heatmap.numpy())

    heatmap = tf.maximum(heatmap, 0) / max_val
    return heatmap.numpy()


def overlay_heatmap_on_image(original_image, heatmap, alpha=0.45):
    heatmap = np.uint8(255 * heatmap)

    jet = matplotlib.colormaps["jet"]
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    jet_heatmap = Image.fromarray(np.uint8(jet_heatmap * 255))
    jet_heatmap = jet_heatmap.resize(original_image.size)

    original_array = np.array(original_image, dtype=np.float32)
    heatmap_array = np.array(jet_heatmap, dtype=np.float32)

    superimposed = heatmap_array * alpha + original_array
    superimposed = np.clip(superimposed, 0, 255).astype(np.uint8)

    return Image.fromarray(superimposed)
