import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection

def detect_face(image_path):

    image = cv2.imread(image_path)

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    detector = mp_face.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    )

    results = detector.process(rgb)

    return results
def crop_face(image_path):

    image = cv2.imread(image_path)

    h, w, _ = image.shape

    detector = mp_face.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    )

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    results = detector.process(rgb)

    if not results.detections:
        return None

    box = results.detections[0].location_data.relative_bounding_box

    x = int(box.xmin * w)
    y = int(box.ymin * h)
    bw = int(box.width * w)
    bh = int(box.height * h)

    face = image[y:y+bh, x:x+bw]

    return face