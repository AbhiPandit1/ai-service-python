import numpy as np

def analyze_voice(audio_chunk):

    volume = np.linalg.norm(audio_chunk)

    silent = volume < 5
    loud = volume > 80

    anomaly = silent or loud

    return {
        "silent": silent,
        "loudNoise": loud,
        "voiceAnomaly": anomaly
    }
