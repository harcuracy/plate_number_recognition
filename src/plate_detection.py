import cv2
import numpy as np
from ultralytics import YOLO
import os

class PlateDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.last_boxes = {}

    def crop_inner_plate(self, crop, top_bottom_ratio=0.2, side_ratio=0.05, pad_ratio=0.1):
        """Crop smaller part of plate and add white padding on left & right."""
        h, w, _ = crop.shape

        # Crop inside plate
        top = int(h * top_bottom_ratio)
        bottom = int(h * (1 - top_bottom_ratio))
        left = int(w * side_ratio)
        right = int(w * (1 - side_ratio))
        crop = crop[top:bottom, left:right]

        # Add white padding left & right
        pad = int(crop.shape[1] * pad_ratio)  # 10% of width by default
        crop_padded = cv2.copyMakeBorder(
            crop, 
            top=0, bottom=0, left=pad, right=pad, 
            borderType=cv2.BORDER_CONSTANT, 
            value=[255, 255, 255]  # white padding
        )
        return crop_padded

    # Detect from single image
    def detect_plates(self, image_path, save_crops=True, crop_folder="cropped_plates"):
        img = cv2.imread(image_path)
        results = self.model.predict(img)
        cropped_paths = []
        os.makedirs(crop_folder, exist_ok=True)

        for result in results:
            for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):
                x1, y1, x2, y2 = map(int, box[:4])
                crop = img[y1:y2, x1:x2]

                # Apply crop + padding
                crop = self.crop_inner_plate(crop)

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

        for result in results:
            for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):
                x1, y1, x2, y2 = map(int, box[:4])
                crop = frame[y1:y2, x1:x2]

                # Apply crop + padding
                crop = self.crop_inner_plate(crop)

                crop_name = f"frame_crop_{i}.jpg"
                crop_path = os.path.join(crop_folder, crop_name)
                if save_crops:
                    cv2.imwrite(crop_path, crop)
                cropped_paths.append(crop_path)
                self.last_boxes[crop_path] = (x1, y1, x2, y2)
        return cropped_paths
