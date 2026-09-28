import sqlite3
from datetime import datetime
import uuid


DB_NAME = "data/measure_verify.db"


# -----------------------------------------
# CREATE VERIFICATION APPLICATION
# -----------------------------------------

def create_application(
    instrument_id,
    applicant_username,
    applicant_name,
    verification_type
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Generate unique application number
    application_number = (
        "APP-" + str(uuid.uuid4())[:8].upper()
    )

    application_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO applications
        (
            application_number,
            instrument_id,
            applicant_username,
            application_type,
            submitted_date,
            status,
            application_id,
            applicant_name,
            verification_type,
            application_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        application_number,
        instrument_id,
        applicant_username,
        verification_type,
        application_date,
        "Pending",
        application_number,
        applicant_name,
        verification_type,
        application_date
    ))

    conn.commit()

    conn.close()

    return application_number


# -----------------------------------------
# GET USER APPLICATIONS
# -----------------------------------------

def get_user_applications(applicant_username):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            application_number,
            instrument_id,
            application_type,
            submitted_date,
            scheduled_date,
            assigned_to,
            status,
            remarks
        FROM applications
        WHERE applicant_username = ?
        ORDER BY id DESC
    """, (
        applicant_username,
    ))

    applications = cursor.fetchall()

    conn.close()

    return applications