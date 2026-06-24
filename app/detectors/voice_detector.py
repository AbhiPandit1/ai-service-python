def detect_noise(audio_level):

    if audio_level is None:
        return False

    # simple thresholds (real systems use similar)

    # too loud (someone talking loudly / external sound)
    if audio_level > 0.25:
        return True

    # too silent for long time (mic muted / no presence)
    if audio_level < 0.01:
        return True

    return False
