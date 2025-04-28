# frontend/app.py

import streamlit as st
import requests

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

st.title("PowerPrompt Gallery")


search_query = st.text_input("Search by Prompt")


# search_query = st.text_input("Search by Prompt") satırının altına ekle

model_filter = st.selectbox(
    "Filter by Model Type",
    ["All", "OpenAI Sora", "Meta Llama", "Other"]
)

style_filter = st.selectbox(
    "Filter by Style Type",
    ["All", "Anime", "Pixelart", "Paint Brush", "Other"]
)


# --- Görsel Yükleme ---
st.header("Upload a New Image")

with st.form("upload_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    prompt = st.text_input("Prompt")
    model_type = st.selectbox("Model Type", ["OpenAI Sora", "Meta Llama", "Other"])
    style_type = st.selectbox("Style Type", ["Anime", "Pixelart", "Paint Brush", "Other"])
    submit = st.form_submit_button("Upload")

    if submit and uploaded_file:
        files = {"file": uploaded_file}
        data = {
            "prompt": prompt,
            "model_type": model_type,
            "style_type": style_type
        }
        response = requests.post(f"{BACKEND_URL}/upload/", files=files, data=data)
        if response.status_code == 200:
            st.success("Upload successful!")
        else:
            st.error(f"Upload failed: {response.text}")

# --- Tüm Görselleri Listeleme ---
st.header("Gallery")

params = {}
if search_query:
    params["query"] = search_query
if model_filter != "All":
    params["model_type"] = model_filter
if style_filter != "All":
    params["style_type"] = style_filter

response = requests.get(f"{BACKEND_URL}/search/", params=params)

if response.status_code == 200:
    images = response.json()

    # Görselleri 3 sütun halinde göster
    cols = st.columns(3)

    for idx, img in enumerate(images):
        with cols[idx % 3]:
            st.image(img["image_url"], use_container_width=True)
            st.caption(f"{img['prompt']} ({img['model_type']}, {img['style_type']})")
else:
    st.error("Failed to load gallery.")
