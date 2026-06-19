import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh


def detect_face_shape(face):

    h, w, _ = face.shape

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1
    ) as mesh:

        rgb = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2RGB
        )

        results = mesh.process(rgb)

        if not results.multi_face_landmarks:
            return "Unknown"

        lm = results.multi_face_landmarks[0].landmark

        left = lm[234]
        right = lm[454]

        top = lm[10]
        chin = lm[152]

        face_width = abs(
            right.x - left.x
        ) * w

        face_height = abs(
            chin.y - top.y
        ) * h

        ratio = face_height / face_width

        if ratio > 1.55:
            return "Oval"

        elif ratio > 1.35:
            return "Heart"

        elif ratio > 1.15:
            return "Round"

        else:
            return "Square"