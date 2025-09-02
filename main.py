from src.plate_detection import PlateDetector



if __name__ == "__main__":
        detector = PlateDetector(model_path="C:/Users/Tumininu Aiyegbusi/Desktop/plate_number_recognition/weights/best.pt")
        # Use an existing image in the environment
        image_path = "C:/Users/Tumininu Aiyegbusi/Desktop/plate_number_recognition/data/image1.jpeg"
        cropped_images = detector.detect_plates(image_path)
        print(f"Cropped images saved: {cropped_images}")