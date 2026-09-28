import sqlite3
import os
import hashlib


DB_NAME = "data/measure_verify.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# ADD MISSING COLUMN SAFELY
# ============================================================

def add_column_if_missing(cursor, table, column, definition):

    columns = [
        row[1]
        for row in cursor.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()
    ]

    if column not in columns:

        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    os.makedirs("data", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # ========================================================
    # USERS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    add_column_if_missing(
        cursor, "users", "password_hash", "TEXT"
    )

    add_column_if_missing(
        cursor, "users", "role", "TEXT"
    )

    add_column_if_missing(
        cursor, "users", "full_name", "TEXT"
    )

    # ========================================================
    # INSTRUMENTS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument_number TEXT UNIQUE NOT NULL,
            instrument_type TEXT NOT NULL,
            manufacturer TEXT,
            model TEXT,
            capacity TEXT,
            owner_name TEXT NOT NULL,
            location TEXT,
            registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Active'
        )
    """)

    # ========================================================
    # APPLICATIONS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_number TEXT UNIQUE NOT NULL,
            instrument_id INTEGER NOT NULL,
            applicant_username TEXT NOT NULL,
            application_type TEXT NOT NULL,
            submitted_date TEXT DEFAULT CURRENT_TIMESTAMP,
            scheduled_date TEXT,
            assigned_to TEXT,
            status TEXT DEFAULT 'Pending',
            remarks TEXT,
            application_id TEXT,
            applicant_name TEXT,
            verification_type TEXT,
            application_date TEXT
        )
    """)

    # ========================================================
    # INSPECTIONS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            inspector_username TEXT NOT NULL,
            inspection_date TEXT DEFAULT CURRENT_TIMESTAMP,
            observations TEXT,
            result TEXT,
            failure_count INTEGER DEFAULT 0,
            evidence_file TEXT,
            remarks TEXT
        )
    """)

    # ========================================================
    # CERTIFICATES
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_number TEXT UNIQUE NOT NULL,
            application_id INTEGER NOT NULL,
            instrument_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            valid_until TEXT NOT NULL,
            verification_result TEXT NOT NULL,
            certificate_data TEXT NOT NULL,
            record_hash TEXT NOT NULL,
            qr_data TEXT,
            status TEXT DEFAULT 'VALID'
        )
    """)

    # ========================================================
    # RISK RECORDS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument_id INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            risk_score INTEGER DEFAULT 0,
            failure_count INTEGER DEFAULT 0,
            overdue_flag INTEGER DEFAULT 0,
            abnormal_pattern_flag INTEGER DEFAULT 0,
            analysis_date TEXT DEFAULT CURRENT_TIMESTAMP,
            explanation TEXT
        )
    """)

    # ========================================================
    # AUDIT LOGS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT,
            entity_id INTEGER,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            details TEXT
        )
    """)

    # ========================================================
    # CREATE / UPDATE DEMO USERS
    # ========================================================

    demo_users = [
        (
            "Demo User",
            "user",
            "user123",
            "User"
        ),
        (
            "Demo LMO",
            "lmo",
            "lmo123",
            "LMO"
        ),
        (
            "Demo GATC",
            "gatc",
            "gatc123",
            "GATC"
        ),
        (
            "System Administrator",
            "admin",
            "admin123",
            "Admin"
        )
    ]

    for full_name, username, password, role in demo_users:

        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        existing = cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        if existing:

            cursor.execute(
                """
                UPDATE users
                SET full_name = ?,
                    password_hash = ?,
                    role = ?
                WHERE username = ?
                """,
                (
                    full_name,
                    password_hash,
                    role,
                    username
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO users
                (
                    full_name,
                    username,
                    password_hash,
                    role
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    full_name,
                    username,
                    password_hash,
                    role
                )
            )

    conn.commit()
    conn.close()


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    initialize_database()

    print(
        "MEASURE VERIFY database initialized successfully."
    )