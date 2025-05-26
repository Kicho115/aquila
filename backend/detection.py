# yolo_utils.py
from ultralytics import YOLO
import cv2

# Carga el modelo solo una vez
yolo_model = YOLO('YOLOv8/runs/detect/train/weights/last.pt')

def detect_y_draw(frame):
    results = yolo_model(frame, verbose=False)[0]
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        label = f"{yolo_model.names[cls]} {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    return frame