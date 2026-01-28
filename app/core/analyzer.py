from app.detectors.face_detector import detect_face
from app.detectors.multi_face import detect_multi
from app.detectors.eye_detector import detect_eye
from app.detectors.head_pose import estimate_head_pose
import numpy as np


def to_bool(val):
    if isinstance(val, (list, tuple, np.ndarray)):
        return len(val) > 0
    return bool(val)


def analyze(frame):

    face_raw = detect_face(frame)
    multi_raw = detect_multi(frame)
    eyes_raw = detect_eye(frame)
    pose_raw = estimate_head_pose(frame)

    face = to_bool(face_raw)
    multi = to_bool(multi_raw)
    eyes = to_bool(eyes_raw)
    pose = to_bool(pose_raw)

    cheating = 0

    if not face:
        cheating += 40

    if multi:
        cheating += 40

    if eyes:
        cheating += 10

    if pose:
        cheating += 10

    return {
        "faceDetected": face,
        "multipleFaces": multi,
        "eyesAway": eyes,
        "headPose": pose,
        "cheatingScore": cheating
    }
