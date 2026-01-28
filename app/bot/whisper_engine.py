import whisper
import numpy as np
import tempfile
import soundfile as sf
import os
import torch

HF_MODEL_PATH = os.path.expanduser("~/.cache/whisper/tiny.pt")

_model = None

def get_model():
    global _model

    if _model is None:
        print("🚀 Loading Whisper tiny from local file...")

        _model = whisper.load_model(
            "tiny",
            download_root=None,
            in_memory=False
        )

        # Force load weights manually
        state = torch.load(HF_MODEL_PATH, map_location="cpu")
        _model.load_state_dict(state)

        print("✅ Whisper loaded from local cache")

    return _model


def transcribe_audio(pcm_bytes):

    audio = np.frombuffer(pcm_bytes, np.int16).astype("float32") / 32768.0

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        sf.write(f.name, audio, 16000)
        path = f.name

    model = get_model()

    result = model.transcribe(path, fp16=False)

    os.remove(path)

    return result["text"].strip()


###cd video-interview-platform/ai-service
### ai-service % source venv/bin/activate