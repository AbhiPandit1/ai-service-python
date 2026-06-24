import cv2
import mediapipe as mp

_mesh = None
def _get_mesh():
    global _mesh
    if _mesh is None:
        _mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    return _mesh

def detect_eye(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    res = _get_mesh().process(rgb)
    if res.multi_face_landmarks:
        lm = res.multi_face_landmarks[0].landmark
        if abs(lm[33].x - lm[263].x) < 0.12:
            return True
    return False
