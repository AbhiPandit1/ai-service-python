import time

def sync_screen(frame_meta):

    return {
        "screenFrameId": frame_meta.get("frameId"),
        "timestamp": time.time()
    }
