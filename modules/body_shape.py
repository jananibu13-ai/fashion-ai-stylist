import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose


def get_distance(p1, p2, w, h):
    x1, y1 = int(p1.x * w), int(p1.y * h)
    x2, y2 = int(p2.x * w), int(p2.y * h)

    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def detect_body_shape(image):

    h, w, _ = image.shape

    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1
    ) as pose:

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb)

        if not results.pose_landmarks:
            return "Unknown"

        lm = results.pose_landmarks.landmark

        left_shoulder = lm[11]
        right_shoulder = lm[12]

        left_hip = lm[23]
        right_hip = lm[24]

        shoulder_width = get_distance(
            left_shoulder,
            right_shoulder,
            w,
            h
        )

        hip_width = get_distance(
            left_hip,
            right_hip,
            w,
            h
        )

        waist_width = hip_width * 0.85

        shoulder_hip_ratio = shoulder_width / hip_width

        waist_hip_ratio = waist_width / hip_width

        if (
            abs(shoulder_width - hip_width) < 25
            and waist_hip_ratio < 0.85
        ):
            return "Hourglass"

        elif hip_width > shoulder_width * 1.10:
            return "Pear"

        elif shoulder_width > hip_width * 1.10:
            return "Inverted Triangle"

        elif waist_hip_ratio > 0.90:
            return "Apple"

        else:
            return "Rectangle"