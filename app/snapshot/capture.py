import base64
import numpy as np
import cv2

from app.core.analyzer import analyze


def process_frame(b64):

    img_bytes = base64.b64decode(b64)

    np_img = np.frombuffer(img_bytes, np.uint8)

    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    return analyze(frame)
