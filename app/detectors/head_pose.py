import cv2
import mediapipe as mp
import numpy as np

_face_mesh = None
def _get_mesh():
    global _face_mesh
    if _face_mesh is None:
        _face_mesh = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True, max_num_faces=1,
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
    return _face_mesh

def get_head_pose(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = _get_mesh().process(rgb)
    if not results.multi_face_landmarks:
        return "CENTER"
    lm = results.multi_face_landmarks[0].landmark
    h, w, _ = image.shape
    face_2d, face_3d = [], []
    for idx in [1, 33, 263, 61, 291, 199]:
        x, y = int(lm[idx].x * w), int(lm[idx].y * h)
        face_2d.append([x, y])
        face_3d.append([x, y, lm[idx].z * 3000])
    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)
    focal_length = w
    cam_matrix = np.array([[focal_length,0,w/2],[0,focal_length,h/2],[0,0,1]], dtype=np.float64)
    dist_coeffs = np.zeros((4,1), dtype=np.float64)
    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_coeffs)
    if not success:
        return "CENTER"
    rmat, _ = cv2.Rodrigues(rot_vec)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    yaw, pitch = angles[1], angles[0]
    if yaw > 12: return "RIGHT"
    elif yaw < -12: return "LEFT"
    elif pitch > 12: return "UP"
    elif pitch < -12: return "DOWN"
    return "CENTER"
