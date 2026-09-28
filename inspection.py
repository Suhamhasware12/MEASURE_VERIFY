import sqlite3
from datetime import datetime

DB_NAME = "data/measure_verify.db"


def schedule_inspection(application_id, scheduled_date, inspector_username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET scheduled_date = ?,
            assigned_to = ?,
            status = 'Scheduled'
        WHERE id = ?
    """, (
        scheduled_date,
        inspector_username,
        application_id
    ))

    conn.commit()
    conn.close()

    return True


def get_pending_applications():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.id,
            a.application_number,
            a.applicant_name,
            a.applicant_username,
            a.instrument_id,
            a.verification_type,
            a.application_date,
            a.status,
            i.instrument_number,
            i.instrument_type,
            i.manufacturer,
            i.model,
            i.capacity,
            i.location
        FROM applications a
        LEFT JOIN instruments i
            ON a.instrument_id = i.id
        WHERE a.status = 'Pending'
        ORDER BY a.id DESC
    """)

    applications = cursor.fetchall()
    conn.close()

    return applications


def get_scheduled_applications(inspector_username):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.id,
            a.application_number,
            a.applicant_name,
            a.instrument_id,
            a.verification_type,
            a.scheduled_date,
            a.assigned_to,
            a.status,
            i.instrument_number,
            i.instrument_type,
            i.manufacturer,
            i.model,
            i.capacity,
            i.location
        FROM applications a
        LEFT JOIN instruments i
            ON a.instrument_id = i.id
        WHERE a.assigned_to = ?
        AND a.status = 'Scheduled'
        ORDER BY a.scheduled_date ASC
    """, (inspector_username,))

    applications = cursor.fetchall()
    conn.close()

    return applications


def record_inspection(
    application_id,
    inspector_username,
    observations,
    result,
    failure_count,
    remarks
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inspection_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO inspections
        (
            application_id,
            inspector_username,
            inspection_date,
            observations,
            result,
            failure_count,
            remarks
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        application_id,
        inspector_username,
        inspection_date,
        observations,
        result,
        failure_count,
        remarks
    ))

    if result == "PASS":
        new_status = "Verified"
    else:
        new_status = "Rejected"

    cursor.execute("""
        UPDATE applications
        SET status = ?,
            remarks = ?
        WHERE id = ?
    """, (
        new_status,
        remarks,
        application_id
    ))

    conn.commit()
    conn.close()

    return True


def get_inspection_history(application_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            application_id,
            inspector_username,
            inspection_date,
            observations,
            result,
            failure_count,
            evidence_file,
            remarks
        FROM inspections
        WHERE application_id = ?
        ORDER BY id DESC
    """, (application_id,))

    inspections = cursor.fetchall()
    conn.close()

    return inspections