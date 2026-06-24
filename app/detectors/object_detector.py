from ultralytics import YOLO

# Load once (important for performance)
print("⏳ Loading YOLO object detector...")
model = YOLO("yolov8n.pt")
print("✅ YOLO object detector loaded")

# COCO class IDs
PERSON_ID = 0
PHONE_ID = 67
BOOK_ID = 73
LAPTOP_ID = 63


def detect_objects(frame, conf_threshold=0.25):

    results = model(frame, verbose=False)[0]

    person_count = 0
    phone = False
    book = False
    laptop = False

    phone_conf = 0.0
    book_conf = 0.0

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if conf < conf_threshold:
            continue

        if cls == PERSON_ID:
            person_count += 1

        elif cls == PHONE_ID:
            phone = True
            phone_conf = max(phone_conf, conf)

        elif cls == BOOK_ID:
            book = True
            book_conf = max(book_conf, conf)

        elif cls == LAPTOP_ID:
            laptop = True

    return {
        "personCount": person_count,
        "phoneDetected": phone,
        "phoneConfidence": round(phone_conf, 2),
        "bookDetected": book,
        "bookConfidence": round(book_conf, 2),
        "laptopDetected": laptop
    }
