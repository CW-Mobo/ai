from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image


def init_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []

    if "selected_example" not in st.session_state:
        st.session_state.selected_example = None

    if "selected_analysis_index" not in st.session_state:
        st.session_state.selected_analysis_index = 0

    if "last_history_key" not in st.session_state:
        st.session_state.last_history_key = None


def add_to_history(file_name, predicted_class, confidence):
    display_confidence = limit_display_confidence(confidence)
    entry = {
        "file_name": file_name,
        "predicted_class": predicted_class,
        "confidence": f"{display_confidence:.2%}",
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    st.session_state.history.insert(0, entry)
    st.session_state.history = st.session_state.history[:10]


def register_history_once(result):
    history_key = (
        result["file_name"],
        result["predicted_class"],
        f"{result['confidence']:.4f}"
    )

    if st.session_state.last_history_key != history_key:
        add_to_history(
            result["file_name"],
            result["predicted_class"],
            result["confidence"]
        )
        st.session_state.last_history_key = history_key


def build_selected_images(uploaded_files):
    selected_images = []

    if uploaded_files:
        for uploaded_file in uploaded_files:
            selected_images.append({
                "name": uploaded_file.name,
                "image": Image.open(uploaded_file).convert("RGB")
            })
    elif st.session_state.selected_example is not None:
        selected_images.append({
            "name": Path(st.session_state.selected_example).name,
            "image": Image.open(st.session_state.selected_example).convert("RGB")
        })

    if not selected_images:
        st.session_state.selected_analysis_index = 0
    elif st.session_state.selected_analysis_index >= len(selected_images):
        st.session_state.selected_analysis_index = 0

    return selected_images
