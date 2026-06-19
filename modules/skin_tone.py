import numpy as np
from sklearn.cluster import KMeans

def get_skin_tone(face_img):

    pixels = face_img.reshape(-1, 3)

    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    kmeans.fit(pixels)

    dominant_color = kmeans.cluster_centers_[0]

    brightness = np.mean(dominant_color)

    if brightness > 180:
        return "Fair"

    elif brightness > 120:
        return "Medium"

    else:
        return "Dark"