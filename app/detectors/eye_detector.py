import cv2
import mediapipe as mp

mp_mesh = mp.solutions.face_mesh
mesh = mp_mesh.FaceMesh(refine_landmarks=True)

def detect_eye(image):

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    res = mesh.process(rgb)

    away = False

    if res.multi_face_landmarks:
        lm = res.multi_face_landmarks[0].landmark
        left = lm[33]
        right = lm[263]

        if abs(left.x - right.x) < 0.12:
            away = True

    return away
