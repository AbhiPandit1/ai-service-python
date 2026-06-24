from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.analyzer import analyze_frame

app = FastAPI()


# ================= CORS =================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= HEALTH =================

@app.get("/")
def root():
    return {"status": "AI Proctor running"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "proctor-api"}


# ================= ANALYZE =================

@app.post("/analyze")
async def analyze(request: Request):

    audio_level = request.query_params.get("audio")

    if audio_level is not None:
        try:
            audio_level = float(audio_level)
        except:
            audio_level = None

    image_bytes = await request.body()

    result = analyze_frame(image_bytes, audio_level)

    return result
