# Proctor service (FastAPI) — only the /analyze path is deployed:
# main:app -> app.core.analyzer -> mediapipe detectors + ultralytics YOLO.
# Whisper/soundfile (voice/WebSocket path) are intentionally NOT installed.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# System libraries required by OpenCV + MediaPipe at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# CPU-only torch first, so ultralytics doesn't pull the multi-GB CUDA build
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
      torch torchvision

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# App code + YOLO weights (object_detector loads ./yolov8n.pt at import time)
COPY main.py .
COPY app ./app
COPY yolov8n.pt .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
