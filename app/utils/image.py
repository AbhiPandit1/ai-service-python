import cv2
import numpy as np

def decode_image(image_bytes):
    return cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )
