from paddleocr import PaddleOCR
import cv2
import os

class PlateRecognizer:
    def __init__(self):
        # Initialize PaddleOCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def recognize_plate(self, image_path, min_conf=0.6):
        # Read the image
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"❌ Error: Could not read image from {image_path}")
            return ""

        # Run OCR
        result = self.ocr.ocr(frame)

        # Debug: print the raw result
        #print(f"\n🔍 Full OCR result for {image_path}:")
        #print(result)

        recognized_info = []

        # Handle dictionary-based result (newer PaddleOCR versions return this)
        if result and isinstance(result, list):
            for page in result:
                if isinstance(page, dict) and "rec_texts" in page:
                    for text, score in zip(page["rec_texts"], page["rec_scores"]):
                        if score >= min_conf:
                            recognized_info.append({"text": text, "confidence": score})
                elif isinstance(page, list):  # old structure
                    for line in page:
                        if len(line) >= 2 and isinstance(line[1], (list, tuple)):
                            text, score = line[1]
                            if score >= min_conf:
                                recognized_info.append({"text": text, "confidence": score})

        # Post-processing: fix common mistakes
        for info in recognized_info:
            info["text"] = (
                info["text"].replace(" ", "")
                            .replace("O", "0")
                            .replace("I", "1")
                            .replace("L", "1")
                            .replace("-", "")
            )

        if recognized_info:
            return recognized_info[0]["text"]
        else:
            return ""