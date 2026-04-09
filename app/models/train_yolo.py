from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="Dataset/meditrust.yaml", epochs=50, imgsz=640, batch=8, name="yolo_meditrust_sig")
