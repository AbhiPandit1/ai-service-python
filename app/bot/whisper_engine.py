import whisper
import numpy as np
import tempfile
import soundfile as sf
import os

# ===============================
# Load model once (startup)
# ===============================

_model = None


def get_model():
    global _model

    if _model is None:
        print("🚀 Loading Whisper tiny model (cached)...")

        # This automatically uses ~/.cache/whisper/tiny.pt
        _model = whisper.load_model("tiny")

        print("✅ Whisper ready")

    return _model


# ===============================
# Transcription function
# ===============================

def transcribe_audio(pcm_bytes: bytes) -> str:
    """
    pcm_bytes: raw 16-bit PCM audio bytes @ 16kHz
    returns transcribed text
    """

    # Convert PCM → float32 waveform
    audio = np.frombuffer(pcm_bytes, np.int16).astype("float32") / 32768.0

    # Write temp wav (Whisper expects file input)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        sf.write(f.name, audio, 16000)
        path = f.name

    try:
        model = get_model()

        result = model.transcribe(
            path,
            fp16=False,      # CPU safe
            language="en"
        )

        return result.get("text", "").strip()

    finally:
        if os.path.exists(path):
            os.remove(path)


###cd video-interview-platform/ai-service
### ai-service % source venv/bin/activate