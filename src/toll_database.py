import sqlite3
from datetime import datetime

# =========================
# Database Initialization
# =========================
def init_db(db_name="toll_system.db"):
    """Initialize database and create table if not exists"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS toll_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT NOT NULL,
        toll_charge INTEGER NOT NULL,
        time TEXT NOT NULL
    )
    """)
    conn.commit()
    return conn, cursor


# =========================
# Insert Record
# =========================
def insert_record(cursor, conn, plate_number, toll_charge=200):
    """Insert vehicle record into database"""
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO toll_records (plate_number, toll_charge, time)
        VALUES (?, ?, ?)
    """, (plate_number, toll_charge, time_now))
    conn.commit()
    print(f"[INFO] Inserted: {plate_number} | Charge: {toll_charge} | Time: {time_now}")


# =========================
# Fetch Records
# =========================
def fetch_records(cursor):
    """Fetch all toll records"""
    cursor.execute("SELECT * FROM toll_records")
    return cursor.fetchall()


# =========================
# Example Usage (Run this file directly)
# =========================
if __name__ == "__main__":
    conn, cursor = init_db()

    # Example inserts
    insert_record(cursor, conn, "EKY 345 AB")
    insert_record(cursor, conn, "AAA 567 XY")
    insert_record(cursor, conn, "GGE 890 LM")

    # Fetch and display
    print("\nAll Toll Records:")
    for row in fetch_records(cursor):
        print(row)

    conn.close()
