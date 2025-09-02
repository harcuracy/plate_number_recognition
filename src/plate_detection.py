import cv2
from ultralytics import YOLO
import os

class PlateDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.last_boxes = {}

    # Detect from single image
    def detect_plates(self, image_path, save_crops=True, crop_folder="cropped_plates"):
        img = cv2.imread(image_path)
        results = self.model.predict(img)
        cropped_paths = []
        os.makedirs(crop_folder, exist_ok=True)

        for result in results:  # Iterate through the list of results
            for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):  # Access boxes from each result
                x1, y1, x2, y2 = map(int, box[:4])
                crop = img[y1:y2, x1:x2]
                crop_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_{i}.jpg"
                crop_path = os.path.join(crop_folder, crop_name)
                if save_crops:
                    cv2.imwrite(crop_path, crop)
                cropped_paths.append(crop_path)
                self.last_boxes[crop_path] = (x1, y1, x2, y2)
        return cropped_paths

    # Detect from live frame
    def detect_plates_from_frame(self, frame, save_crops=True, crop_folder="cropped_plates"):
        results = self.model.predict(frame)
        cropped_paths = []
        os.makedirs(crop_folder, exist_ok=True)

        for result in results:  # Iterate through the list of results
            for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):  # Access boxes from each result
                x1, y1, x2, y2 = map(int, box[:4])
                crop = frame[y1:y2, x1:x2]
                crop_name = f"frame_crop_{i}.jpg"
                crop_path = os.path.join(crop_folder, crop_name)
                if save_crops:
                    cv2.imwrite(crop_path, crop)
                cropped_paths.append(crop_path)
                self.last_boxes[crop_path] = (x1, y1, x2, y2)
        return cropped_paths