from app.detectors.ml_classifier import classify

def calculate_score(flags):

    score = 0

    if flags["noFace"]:
        score += 30

    if flags["multipleFaces"]:
        score += 40

    if flags["eyesAway"]:
        score += 15

    if flags["phoneDetected"]:
        score += 50

    if flags.get("headLookingAway"):
        score += 20

    score = min(score, 100)

    ml = classify(flags, score)

    return score, ml
