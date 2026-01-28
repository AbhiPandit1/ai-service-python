import cv2
import mediapipe as mp

mp_mesh = mp.solutions.face_mesh
mesh = mp_mesh.FaceMesh(refine_landmarks=True)

def detect_eye_direction(image):

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = mesh.process(rgb)

    eyes_away = False

    if result.multi_face_landmarks:
        lm = result.multi_face_landmarks[0].landmark

        left_eye = lm[33]
        right_eye = lm[263]

        dist = abs(left_eye.x - right_eye.x)

        if dist < 0.12:
            eyes_away = True

    return {
        "eyesLookingAway": eyes_away
    }
