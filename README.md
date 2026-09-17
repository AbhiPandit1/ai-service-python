# ai-service-python

An **AI proctoring / exam-integrity microservice**. It runs computer-vision
detection over webcam frames — multiple faces, looking-away, phone/object
presence — and returns structured integrity signals. Served as a FastAPI HTTP
service and shipped as a Docker container.

## What it does
- **YOLO-based** person/object detection on incoming frames
- Per-frame analysis to structured proctoring flags (multi-face, away-gaze, device presence)
- **FastAPI** endpoint for real-time scoring
- Containerized; model weights fetched at build time (not committed)

## Stack
Python · Ultralytics YOLO · OpenCV · FastAPI · Docker

## Run
```bash
docker build -t ai-service .
docker run -p 8000:8000 ai-service
# POST a frame:
# curl -F "file=@frame.jpg" http://localhost:8000/analyze
```

## Notes
This repository holds the **ML service layer** extracted from a production
interview platform. It is the computer-vision component; orchestration,
storage, and the interview app live elsewhere.
