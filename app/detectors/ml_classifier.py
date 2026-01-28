import random

# placeholder for trained model

def classify(flags, score):

    risk = score

    if flags.get("headLookingAway"):
        risk += 15

    if flags.get("voiceAnomaly"):
        risk += 10

    risk = min(risk, 100)

    label = "normal"

    if risk > 70:
        label = "high_risk"
    elif risk > 40:
        label = "medium_risk"

    return {
        "mlRiskScore": risk,
        "mlLabel": label
    }
