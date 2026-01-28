from fastapi import FastAPI, UploadFile, File, WebSocket

from app.core.websocket import proctor_socket

app = FastAPI()


# ===============================
# Optional HTTP frame analyze
# (not used in live flow anymore)
# ===============================

@app.post("/analyze-frame")
async def analyze(file: UploadFile = File(...)):

    # Lazy import (prevents startup freeze)
    from app.snapshot.capture import process_frame  

    data = await file.read()

    return process_frame(data)


# ===============================
# WebSocket (main flow)
# ===============================

@app.websocket("/ws/proctor")
async def ws_endpoint(ws: WebSocket):

    await proctor_socket(ws)
