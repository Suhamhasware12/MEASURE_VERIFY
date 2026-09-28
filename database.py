import sqlite3
import os


DB_NAME = "data/measure_verify.db"


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def get_connection():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


# -----------------------------------------
# INITIALIZE DATABASE
# -----------------------------------------

def initialize_database():

    os.makedirs("data", exist_ok=True)

    conn = get_connection()

    cursor = conn.cursor()


    # -----------------------------------------
    # USERS TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)


    # -----------------------------------------
    # INSTRUMENTS TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument_number TEXT UNIQUE NOT NULL,
            instrument_type TEXT NOT NULL,
            manufacturer TEXT,
            model TEXT,
            capacity TEXT,
            owner_name TEXT NOT NULL,
            location TEXT
        )
    """)


    # -----------------------------------------
    # APPLICATIONS TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id TEXT UNIQUE,
            instrument_id INTEGER NOT NULL,
            applicant_name TEXT NOT NULL,
            verification_type TEXT NOT NULL,
            status TEXT NOT NULL,
            application_date TEXT,
            FOREIGN KEY (instrument_id)
                REFERENCES instruments(id)
        )
    """)


    # -----------------------------------------
    # INSPECTIONS TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER,
            inspector_name TEXT,
            inspection_date TEXT,
            observations TEXT,
            result TEXT,
            FOREIGN KEY (application_id)
                REFERENCES applications(id)
        )
    """)


    # -----------------------------------------
    # CERTIFICATES TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER,
            certificate_number TEXT UNIQUE,
            issue_date TEXT,
            expiry_date TEXT,
            certificate_hash TEXT,
            FOREIGN KEY (application_id)
                REFERENCES applications(id)
        )
    """)


    # -----------------------------------------
    # RISK RECORDS TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument_id INTEGER,
            risk_level TEXT,
            risk_score REAL,
            reason TEXT,
            created_at TEXT,
            FOREIGN KEY (instrument_id)
                REFERENCES instruments(id)
        )
    """)


    # -----------------------------------------
    # AUDIT LOGS TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            action TEXT,
            timestamp TEXT
        )
    """)


    # -----------------------------------------
    # APPLICATION TABLE MIGRATION
    # -----------------------------------------

    cursor.execute(
        "PRAGMA table_info(applications)"
    )

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]


    if "application_id" not in columns:

        cursor.execute("""
            ALTER TABLE applications
            ADD COLUMN application_id TEXT
        """)


    if "applicant_name" not in columns:

        cursor.execute("""
            ALTER TABLE applications
            ADD COLUMN applicant_name TEXT
        """)


    if "verification_type" not in columns:

        cursor.execute("""
            ALTER TABLE applications
            ADD COLUMN verification_type TEXT
        """)


    if "status" not in columns:

        cursor.execute("""
            ALTER TABLE applications
            ADD COLUMN status TEXT
        """)


    if "application_date" not in columns:

        cursor.execute("""
            ALTER TABLE applications
            ADD COLUMN application_date TEXT
        """)


    conn.commit()

    conn.close()

    print(
        "MEASURE VERIFY database initialized successfully."
    )


# -----------------------------------------
# RUN DIRECTLY
# -----------------------------------------

if __name__ == "__main__":

    initialize_database()