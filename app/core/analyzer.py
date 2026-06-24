import cv2
import numpy as np

from app.detectors.multi_face import detect_multi_face
from app.detectors.eye_tracker import is_looking_away
from app.detectors.head_pose import get_head_pose
from app.detectors.voice_detector import detect_noise
from app.detectors.object_detector import detect_objects


def analyze_frame(image_bytes, audio_level=None):

    # =======================
    # Decode frame
    # =======================

    npimg = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if frame is None:
        events = {
            "faceCount": 0,
            "presence": False,
            "multipleFace": False,
            "lookingAway": False,
            "headTurn": False,
            "noise": False,
            "phoneDetected": False,
            "bookDetected": False,
            "extraPerson": False
        }

        print("📸 PROCTOR EVENT >>>", events)
        return events


    # =======================
    # FACE COUNT
    # =======================

    face_count = detect_multi_face(frame)

    presence = face_count > 0
    multiple_face = face_count > 1


    # =======================
    # EYES
    # =======================

    looking_away = False
    if face_count >= 1:
        looking_away = is_looking_away(frame)


    # =======================
    # HEAD POSE
    # =======================

    head_turn = False
    if face_count >= 1:
        pose = get_head_pose(frame)
        head_turn = pose in ["LEFT", "RIGHT", "DOWN"]


    # =======================
    # AUDIO
    # =======================

    noise = False
    if audio_level is not None:
        noise = detect_noise(audio_level)


    # =======================
    # OBJECT DETECTION (YOLO)
    # =======================

    objects = detect_objects(frame)

    extra_person = objects["personCount"] > 1


    # =======================
    # FINAL EVENTS
    # =======================

    events = {
        "faceCount": int(face_count),
        "presence": presence,
        "multipleFace": multiple_face,
        "lookingAway": bool(looking_away),
        "headTurn": bool(head_turn),
        "noise": bool(noise),

        "extraPerson": extra_person,

        "phoneDetected": objects["phoneDetected"],
        "phoneConfidence": objects["phoneConfidence"],

        "bookDetected": objects["bookDetected"],
        "bookConfidence": objects["bookConfidence"],

        "laptopDetected": objects["laptopDetected"]
    }

    print("📸 PROCTOR EVENT >>>", events)

    return events
