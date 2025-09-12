# 🚗 Automatic Toll Collection System (ANPR)

This is a **Streamlit web app** for an **Automatic Number Plate Recognition (ANPR)** system at toll gates.  
It detects vehicle number plates from uploaded images, recognizes the plate number, and logs it in a database with a fixed toll charge.

---

## ✨ Features

- Upload vehicle images (`.jpg`, `.jpeg`, `.png`)
- Automatically detect and crop license plates (YOLO model)
- Recognize plate numbers with OCR
- Log recognized plates with toll charges into a database
- View all toll records in a clean Streamlit table

---

## 🛠️ Requirements

- Python 3.8+  
- [uv](https://github.com/astral-sh/uv) (optional, for fast installs)

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/harcuracy/plate_number_recognition.git
cd plate_number_recognition
```

### 2️⃣ Create a virtual environment  
Using **uv**:
```bash
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

Or using built-in `venv`:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies  
If you already have a `requirements.txt`:
```bash
uv pip install -r requirements.txt
```

If you need to create one, include at least:
```txt
streamlit
pandas
opencv-python
torch
torchvision
pillow
sqlalchemy  # or sqlite3 depending on your DB wrapper
```

---

## ⚙️ How to Run

1. Make sure the YOLO model weights are at `weights/best.pt` or update the path in `app.py`.
2. Run the app:

```bash
streamlit run app.py
```

3. Open the URL shown in the terminal (usually http://localhost:8501) in your browser.

---

## 📝 Usage

- Upload a vehicle image.
- The system will:
  - Detect the plate and crop it.
  - Recognize the plate number.
  - Insert the plate number + toll charge (default 200) into the DB.
- Scroll down to see the toll record table.

---

## 📚 Notes

- The detection model is expected to be a YOLOv5/YOLOv8-style model saved as `weights/best.pt`.
- The recognition uses an OCR pipeline in `src/plate_recognition.py`.  
- The database uses SQLite by default through `src/toll_database.py`.

---

## 🖇️ License

MIT License
