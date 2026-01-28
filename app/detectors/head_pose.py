import cv2
import mediapipe as mp
import numpy as np

mp_mesh = mp.solutions.face_mesh
mesh = mp_mesh.FaceMesh(refine_landmarks=True)

def estimate_head_pose(image):

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    res = mesh.process(rgb)

    looking_away = False

    if res.multi_face_landmarks:

        lm = res.multi_face_landmarks[0].landmark

        nose = lm[1]
        left = lm[33]
        right = lm[263]

        yaw = (right.x - left.x) * 100

        if abs(yaw) > 15:
            looking_away = True

    return {
        "headLookingAway": looking_away
    }
