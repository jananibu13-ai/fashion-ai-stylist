import streamlit as st
import sys

st.title("AI Fashion Stylist")
st.write("Python version:", sys.version)

import cv2

st.success("OpenCV loaded successfully")
# TEMPORARILY COMMENT THESE
# import cv2
# import numpy as np
# from PIL import Image

# from modules.face_analysis import crop_face
# from modules.skin_tone import get_skin_tone
# from modules.recommender import recommend_products

uploaded_file = st.file_uploader(
    "Upload Face Image",
    type=["jpg", "jpeg", "png"]
)

gender = st.selectbox(
    "Gender",
    ["Men", "Women"]
)

occasion = st.selectbox(
    "Occasion",
    [
        "Casual",
        "Formal",
        "Sports",
        "Ethnic"
    ]
)
height = st.number_input(
    "Height (cm)",
    min_value=120,
    max_value=220,
    value=165
)

budget = st.slider(
    "Budget",
    500,
    10000,
    3000
)

if st.button("Generate Recommendations"):

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        image_np = np.array(image)

        temp_path = "temp.jpg"

        cv2.imwrite(
            temp_path,
            cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        )

        face = crop_face(temp_path)

        skin_tone = get_skin_tone(face)

        st.subheader("Analysis Results")

        st.metric(
            label="Detected Skin Tone",
            value=skin_tone
        )

        recommendations = recommend_products(
            skin_tone,
            gender,
            occasion
        )

        st.subheader("Recommended Products")

        for _, row in recommendations.iterrows():

            st.write(
                f"👕 {row['productDisplayName']}"
            )

            st.write(
                f"Color: {row['baseColour']}"
            )

            st.write(
                f"Type: {row['articleType']}"
            )

            st.write(
                f"Occasion: {row['usage']}"
            )

            st.divider()

    else:
        st.warning("Please upload an image.")