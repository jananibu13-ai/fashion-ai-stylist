import streamlit as st
import cv2
import numpy as np
from PIL import Image

from modules.face_analysis import crop_face
from modules.skin_tone import get_skin_tone
from modules.recommender import recommend_products
from modules.body_shape import detect_body_shape
from modules.face_shape import detect_face_shape

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Fashion Stylist",
    page_icon="👗",
    layout="wide"
)

st.title("👗 AI Fashion Stylist")
st.markdown(
    "Get personalized fashion recommendations using AI-powered face, skin tone and body shape analysis."
)

# --------------------------------------------------
# STYLE TIPS
# --------------------------------------------------

STYLE_TIPS = {

    "Hourglass": [
        "Wrap Dresses",
        "High Waist Jeans",
        "Fitted Blazers"
    ],

    "Pear": [
        "Boat Neck Tops",
        "Statement Jackets",
        "Structured Shoulders"
    ],

    "Apple": [
        "V Neck Tops",
        "Straight Kurtas",
        "Empire Waist Dresses"
    ],

    "Rectangle": [
        "Layered Outfits",
        "Peplum Tops",
        "Belted Dresses"
    ],

    "Inverted Triangle": [
        "A-line Skirts",
        "Wide Leg Trousers",
        "Flared Bottoms"
    ]
}

FACE_SHAPE_ADVICE = {

    "Oval": [
        "Most hairstyles suit you",
        "Try layered cuts",
        "Experiment with accessories"
    ],

    "Round": [
        "Long layers add definition",
        "V-necks work well",
        "Avoid overly round accessories"
    ],

    "Square": [
        "Soft curls complement jawline",
        "Rounded necklines work well",
        "Avoid boxy silhouettes"
    ],

    "Heart": [
        "Chin-length styles work well",
        "Balance wider forehead",
        "Try statement earrings"
    ]
}

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Preferences")

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

# --------------------------------------------------
# IMAGE UPLOADS
# --------------------------------------------------

st.subheader("Upload Images")

col1, col2 = st.columns(2)

with col1:

    face_file = st.file_uploader(
        "📸 Upload Face Image",
        type=["jpg", "jpeg", "png"],
        key="face"
    )

with col2:

    body_file = st.file_uploader(
        "🧍 Upload Full Body Image",
        type=["jpg", "jpeg", "png"],
        key="body"
    )

# --------------------------------------------------
# PREVIEW
# --------------------------------------------------

if face_file and body_file:

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            face_file,
            caption="Face Image",
            use_container_width=True
        )

    with col2:
        st.image(
            body_file,
            caption="Body Image",
            use_container_width=True
        )

# --------------------------------------------------
# GENERATE
# --------------------------------------------------

if st.button("✨ Generate Recommendations"):

    if face_file is not None and body_file is not None:

        with st.spinner(
            "Analyzing your style profile..."
        ):

            # FACE IMAGE

            face_image = Image.open(face_file)
            face_np = np.array(face_image)

            temp_face = "temp_face.jpg"

            cv2.imwrite(
                temp_face,
                cv2.cvtColor(
                    face_np,
                    cv2.COLOR_RGB2BGR
                )
            )

            face = crop_face(temp_face)

            skin_tone = get_skin_tone(face)

            face_shape = detect_face_shape(face)

            # BODY IMAGE

            body_image = Image.open(body_file)

            body_np = np.array(body_image)

            body_shape = detect_body_shape(body_np)

            # RECOMMENDATIONS

            recommendations = recommend_products(
                skin_tone,
                gender,
                occasion,
                body_shape
            )

        # --------------------------------------------------
        # RESULTS
        # --------------------------------------------------

        st.header("✨ Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🎨 Skin Tone",
                skin_tone
            )

        with col2:
            st.metric(
                "📏 Body Shape",
                body_shape
            )

        with col3:
            st.metric(
                "🙂 Face Shape",
                face_shape
            )

        # --------------------------------------------------
        # STYLE ADVICE
        # --------------------------------------------------

        st.header("💡 Personal Style Advice")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Body Shape Tips")

            for tip in STYLE_TIPS.get(
                body_shape,
                []
            ):
                st.success(tip)

        with col2:

            st.subheader("Face Shape Tips")

            for tip in FACE_SHAPE_ADVICE.get(
                face_shape,
                []
            ):
                st.info(tip)

        # --------------------------------------------------
        # PRODUCTS
        # --------------------------------------------------

        st.header("🛍 Recommended Products")

        if recommendations.empty:

            st.warning(
                "No matching products found."
            )

        else:

            for _, row in recommendations.iterrows():

                with st.container():

                    st.markdown(
                        f"""
### 👕 {row['productDisplayName']}

**Color:** {row['baseColour']}

**Type:** {row['articleType']}

**Occasion:** {row['usage']}
"""
                    )

                    st.divider()

    else:

        st.warning(
            "Please upload both face and body images."
        )