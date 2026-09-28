import sqlite3
import hashlib
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

DB_NAME = "data/measure_verify.db"

CERTIFICATE_FOLDER = Path("certificates")
CERTIFICATE_FOLDER.mkdir(exist_ok=True)


def generate_record_hash(certificate_data):
    """
    Generate a SHA-256 hash for the certificate record.
    """

    data_string = json.dumps(
        certificate_data,
        sort_keys=True
    )

    return hashlib.sha256(
        data_string.encode("utf-8")
    ).hexdigest()


def create_certificate(
    application_id,
    instrument_id,
    verification_result="VERIFIED",
    validity_days=365
):
    """
    Create a digital verification certificate
    for a successfully verified application.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check whether certificate already exists
    cursor.execute("""
        SELECT certificate_number
        FROM certificates
        WHERE application_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (application_id,))

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return existing[0]

    # Get application and instrument details
    cursor.execute("""
        SELECT
            a.application_number,
            a.applicant_name,
            a.verification_type,
            i.instrument_number,
            i.instrument_type,
            i.manufacturer,
            i.model,
            i.capacity,
            i.owner_name,
            i.location
        FROM applications a
        JOIN instruments i
            ON a.instrument_id = i.id
        WHERE a.id = ?
    """, (application_id,))

    record = cursor.fetchone()

    if not record:
        conn.close()
        return None

    (
        application_number,
        applicant_name,
        verification_type,
        instrument_number,
        instrument_type,
        manufacturer,
        model,
        capacity,
        owner_name,
        location
    ) = record

    issue_date = datetime.now()

    valid_until = issue_date + timedelta(
        days=validity_days
    )

    certificate_number = (
        "CERT-" +
        datetime.now().strftime("%Y%m%d") +
        "-" +
        str(uuid.uuid4())[:6].upper()
    )

    # Certificate information
    certificate_data = {
        "certificate_number": certificate_number,
        "application_number": application_number,
        "application_id": application_id,
        "instrument_id": instrument_id,
        "instrument_number": instrument_number,
        "instrument_type": instrument_type,
        "manufacturer": manufacturer,
        "model": model,
        "capacity": capacity,
        "owner_name": owner_name,
        "location": location,
        "applicant_name": applicant_name,
        "verification_type": verification_type,
        "verification_result": verification_result,
        "issue_date": issue_date.strftime(
            "%Y-%m-%d"
        ),
        "valid_until": valid_until.strftime(
            "%Y-%m-%d"
        )
    }

    # Generate SHA-256 integrity hash
    record_hash = generate_record_hash(
        certificate_data
    )

    # QR data contains certificate reference
    qr_data = json.dumps({
        "certificate_number": certificate_number,
        "application_id": application_id,
        "instrument_number": instrument_number,
        "record_hash": record_hash
    })

    # Store certificate
    cursor.execute("""
        INSERT INTO certificates
        (
            certificate_number,
            application_id,
            instrument_id,
            issue_date,
            valid_until,
            verification_result,
            certificate_data,
            record_hash,
            qr_data,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        certificate_number,
        application_id,
        instrument_id,
        issue_date.strftime(
            "%Y-%m-%d"
        ),
        valid_until.strftime(
            "%Y-%m-%d"
        ),
        verification_result,
        json.dumps(
            certificate_data,
            indent=2
        ),
        record_hash,
        qr_data,
        "VALID"
    ))

    conn.commit()
    conn.close()

    # Save a readable certificate record
    certificate_file = (
        CERTIFICATE_FOLDER /
        f"{certificate_number}.json"
    )

    with open(
        certificate_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            certificate_data,
            file,
            indent=4
        )

    return certificate_number


def get_certificate(certificate_number):
    """
    Retrieve certificate information.
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            certificate_number,
            application_id,
            instrument_id,
            issue_date,
            valid_until,
            verification_result,
            certificate_data,
            record_hash,
            qr_data,
            status
        FROM certificates
        WHERE certificate_number = ?
    """, (certificate_number,))

    certificate = cursor.fetchone()

    conn.close()

    return certificate


def get_certificate_by_application(application_id):
    """
    Retrieve certificate associated with an application.
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            certificate_number,
            application_id,
            instrument_id,
            issue_date,
            valid_until,
            verification_result,
            certificate_data,
            record_hash,
            qr_data,
            status
        FROM certificates
        WHERE application_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (application_id,))

    certificate = cursor.fetchone()

    conn.close()

    return certificate


def get_all_certificates():
    """
    Retrieve all issued certificates.
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.certificate_number,
            c.application_id,
            c.instrument_id,
            i.instrument_number,
            i.instrument_type,
            i.owner_name,
            c.issue_date,
            c.valid_until,
            c.verification_result,
            c.record_hash,
            c.status
        FROM certificates c
        LEFT JOIN instruments i
            ON c.instrument_id = i.id
        ORDER BY c.id DESC
    """)

    certificates = cursor.fetchall()

    conn.close()

    return certificates