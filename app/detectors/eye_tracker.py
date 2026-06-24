import cv2
import mediapipe as mp

_mesh = None

def _get_mesh():
    global _mesh
    if _mesh is None:
        _mesh = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    return _mesh

LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]
LEFT_EYE_INNER = 133
LEFT_EYE_OUTER = 33
RIGHT_EYE_INNER = 362
RIGHT_EYE_OUTER = 263

def _iris_ratio(lm, iris_ids, inner_id, outer_id):
    iris_x = sum(lm[i].x for i in iris_ids) / len(iris_ids)
    inner_x = lm[inner_id].x
    outer_x = lm[outer_id].x
    eye_width = abs(inner_x - outer_x)
    if eye_width < 0.001:
        return 0.5
    return (iris_x - outer_x) / (inner_x - outer_x)

def is_looking_away(image):
    try:
        import mediapipe.python.solutions.face_mesh  # ensure solutions loaded
    except Exception:
        pass
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = _get_mesh().process(rgb)
    if not result.multi_face_landmarks:
        return False
    lm = result.multi_face_landmarks[0].landmark
    left_ratio = _iris_ratio(lm, LEFT_IRIS, LEFT_EYE_INNER, LEFT_EYE_OUTER)
    right_ratio = _iris_ratio(lm, RIGHT_IRIS, RIGHT_EYE_INNER, RIGHT_EYE_OUTER)
    avg_ratio = (left_ratio + right_ratio) / 2
    return avg_ratio < 0.25 or avg_ratio > 0.75
