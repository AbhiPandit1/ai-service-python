from fastapi import WebSocket, WebSocketDisconnect
import json
import base64
import time

from app.snapshot.capture import process_frame
from app.bot.question_engine import QuestionEngine
from app.bot.whisper_engine import transcribe_audio
from app.core.config import ALERT_THRESHOLD, AUTO_DISQUALIFY


async def proctor_socket(ws: WebSocket):

    await ws.accept()

    engine = None
    full_answer = ""
    last_audio_time = time.time()

    try:
        while True:

            msg = await ws.receive_text()
            data = json.loads(msg)

            msg_type = data.get("type")

            # ================= INIT =================

            if msg_type == "INIT":

                role = data.get("role", "mern")

                engine = QuestionEngine(role)

                first_q = engine.next_question()

                await ws.send_json({
                    "type": "QUESTION",
                    "data": first_q
                })

            # ================= VIDEO FRAME =================

            elif msg_type == "FRAME":

                frame_b64 = data["data"]

                result = process_frame(frame_b64)

                await ws.send_json({
                    "type": "PROCTOR",
                    "data": result
                })

                if result["cheatingScore"] >= ALERT_THRESHOLD:
                    await ws.send_json({
                        "type": "PROCTOR",
                        "alert": "Suspicious behaviour detected"
                    })

                if result["cheatingScore"] >= AUTO_DISQUALIFY:
                    await ws.send_json({
                        "type": "PROCTOR",
                        "disqualify": True
                    })
                    break

            # ================= AUDIO → WHISPER =================

            elif msg_type == "AUDIO_CHUNK":

                audio_b64 = data["data"]
                audio_bytes = base64.b64decode(audio_b64)

                text = transcribe_audio(audio_bytes)

                if text:

                    full_answer += " " + text
                    last_audio_time = time.time()

                    await ws.send_json({
                        "type": "ANSWER_LIVE",
                        "data": full_answer.strip()
                    })

            # ================= SILENCE DETECTOR =================

            elif msg_type == "SILENCE_CHECK":

                if engine is None:
                    continue

                # 3 seconds silence
                if time.time() - last_audio_time > 3 and full_answer.strip():

                    engine.record_answer(full_answer.strip())

                    full_answer = ""

                    next_q = engine.next_question()

                    if next_q:
                        await ws.send_json({
                            "type": "QUESTION",
                            "data": next_q
                        })
                    else:
                        await ws.send_json({
                            "type": "INTERVIEW_COMPLETE"
                        })
                        break

    except WebSocketDisconnect:
        print("Client disconnected normally")

    except Exception as e:
        print("WebSocket error:", e)

    finally:
        try:
            await ws.close()
        except:
            pass
