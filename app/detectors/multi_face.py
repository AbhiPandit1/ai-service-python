import cv2
import mediapipe as mp

_detector = None

def _get_detector():
    global _detector
    if _detector is None:
        _detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        )
    return _detector

def detect_multi_face(frame):
    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = _get_detector().process(rgb)
        if not results.detections:
            return 0
        return len(results.detections)
    except Exception:
        return 0
