import mediapipe as mp
import cv2

_detector = None
def get_detector():
    global _detector
    if _detector is None:
        print("Loading face detector...")
        _detector = mp.solutions.face_detection.FaceDetection(0.7)
        print("Face detector loaded")
    return _detector

def detect_face(image):
    result = get_detector().process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return bool(result.detections)
