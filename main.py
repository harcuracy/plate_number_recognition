import os
from src.plate_detection import PlateDetector
from src.plate_recognition import PlateRecognizer

# Import database functions
from src.toll_database import init_db, insert_record, fetch_records

if __name__ == "__main__":
    # 1. Initialize database
    conn, cursor = init_db()

    # 2. Detect plates
    detector = PlateDetector(
        model_path=r"C:/Users/Tumininu Aiyegbusi/Desktop/plate_number_recognition/weights/best.pt"
    )
    image_path = r"C:/Users/Tumininu Aiyegbusi/Desktop/plate_number_recognition/data/image2.jpg"
    cropped_images = detector.detect_plates(image_path)
    print(f"Cropped images saved: {cropped_images}")

    # 3. Recognize plates from cropped images
    recognizer = PlateRecognizer()
    cropped_folder = "cropped_plates"  # folder where cropped plates are saved

    if not os.path.exists(cropped_folder):
        print(f"❌ Error: The folder was not found at {cropped_folder}")
    else:
        for img_file in os.listdir(cropped_folder):
            img_path = os.path.join(cropped_folder, img_file)

            if os.path.isfile(img_path):
                plate_number = recognizer.recognize_plate(img_path, min_conf=0.5)
                print(f"✅ {img_file} → Recognized plate: {plate_number}")

                # 4. Save recognized plate into database with constant toll charge
                if plate_number:  # make sure recognition returned something
                    insert_record(cursor, conn, plate_number, toll_charge=200)

    # 5. Show all stored records
    print("\n📌 All Toll Records in Database:")
    for row in fetch_records(cursor):
        print(row)

    # 6. Close database
    conn.close()
