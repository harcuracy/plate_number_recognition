import streamlit as st
import os
from datetime import datetime

from src.plate_detection import PlateDetector
from src.plate_recognition import PlateRecognizer
from src.toll_database import init_db, insert_record, fetch_records


# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="Toll Gate ANPR", layout="centered")

st.title("🚗 Automatic Toll Collection System")
st.write("Upload a vehicle image, detect the plate, and log it with a fixed charge.")


# Initialize database
conn, cursor = init_db()


# Upload image
uploaded_file = st.file_uploader("Upload vehicle image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Save uploaded file
    image_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Vehicle", use_container_width=True)

    # Detect plate
    detector = PlateDetector(
        model_path="weights/best.pt"  # update with your model path
    )
    cropped_images = detector.detect_plates(image_path)

    if cropped_images:
        st.success(f"Plate cropped and saved: {cropped_images}")

        recognizer = PlateRecognizer()

        for img_file in cropped_images:
            plate_number = recognizer.recognize_plate(img_file, min_conf=0.5)
            if plate_number:
                st.write(f"✅ Recognized Plate: **{plate_number}**")

                # Save to DB with constant charge
                insert_record(cursor, conn, plate_number, toll_charge=200)

# Show DB records
st.subheader("📌 Toll Records")
records = fetch_records(cursor)
if records:
    # Prettify records into a dataframe for Streamlit
    import pandas as pd
    df = pd.DataFrame(records, columns=["ID", "Plate Number", "Toll Charge", "Time"])
    st.dataframe(df)
else:
    st.info("No records found yet.")
