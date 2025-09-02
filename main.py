import os
from src.plate_detection import PlateDetector
from src.plate_recognition import PlateRecognizer

if __name__ == "__main__":
    # 1. Detect plates
    detector = PlateDetector(
        model_path=r"C:/Users/Tumininu Aiyegbusi/Desktop/plate_number_recognition/weights/best.pt"
    )
    image_path = r"C:/Users/Tumininu Aiyegbusi/Desktop/plate_number_recognition/data/image2.jpg"
    cropped_images = detector.detect_plates(image_path)
    print(f"Cropped images saved: {cropped_images}")

    # 2. Recognize plates from cropped images
    recognizer = PlateRecognizer()
    cropped_folder = "cropped_plates"  # folder where cropped plates are saved
    print(cropped_folder)

    if not os.path.exists(cropped_folder):
        print(f"❌ Error: The folder was not found at {cropped_folder}")
    else:
        for img_file in os.listdir(cropped_folder):
            img_path = os.path.join(cropped_folder, img_file)

            if os.path.isfile(img_path):
                plate_number = recognizer.recognize_plate(img_path, min_conf=0.5)
                print(f"✅ {img_file} → Recognized plate: {plate_number}")
