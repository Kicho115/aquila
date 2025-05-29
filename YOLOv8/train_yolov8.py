from ultralytics import YOLO
import os

def main():
    # Ruta al checkpoint
    checkpoint_path = 'runs/detect/train/weights/last.pt'

    # Si existe el checkpoint, reanuda; si no, inicia desde cero
    if os.path.exists(checkpoint_path):
        print(f"Reanudando entrenamiento desde {checkpoint_path}")
        model = YOLO(checkpoint_path)
        resume = True
    else:
        print("Iniciando entrenamiento desde cero (modelo base yolov8n.pt)")
        model = YOLO('yolov8n.pt')
        resume = False

    model.train(
        data='coco.yaml',
        epochs=50,
        imgsz=640,
        batch=8,
        device=0,
        resume=resume
    )

if __name__ == "__main__":
    main()