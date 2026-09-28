import sqlite3
import json
import hashlib
from pathlib import Path

import qrcode


DB_NAME = "data/measure_verify.db"

QR_FOLDER = Path("certificates/qr")
QR_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def generate_qr(certificate_number):
    """
    Generate a QR code for a certificate.
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.certificate_number,
            c.application_id,
            c.instrument_id,
            i.instrument_number,
            c.record_hash,
            c.qr_data
        FROM certificates c
        LEFT JOIN instruments i
            ON c.instrument_id = i.id
        WHERE c.certificate_number = ?
    """, (certificate_number,))

    certificate = cursor.fetchone()

    conn.close()

    if not certificate:
        return None

    qr_content = certificate["qr_data"]

    if not qr_content:
        qr_content = json.dumps({
            "certificate_number":
                certificate["certificate_number"],
            "application_id":
                certificate["application_id"],
            "instrument_id":
                certificate["instrument_id"],
            "instrument_number":
                certificate["instrument_number"],
            "record_hash":
                certificate["record_hash"]
        })

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(qr_content)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    qr_file = (
        QR_FOLDER /
        f"{certificate_number}.png"
    )

    image.save(qr_file)

    return str(qr_file)


def verify_certificate(certificate_number):
    """
    Verify certificate existence and SHA-256 integrity.
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.certificate_number,
            c.application_id,
            c.instrument_id,
            i.instrument_number,
            c.issue_date,
            c.valid_until,
            c.verification_result,
            c.certificate_data,
            c.record_hash,
            c.status
        FROM certificates c
        LEFT JOIN instruments i
            ON c.instrument_id = i.id
        WHERE c.certificate_number = ?
    """, (certificate_number,))

    certificate = cursor.fetchone()

    conn.close()

    if not certificate:
        return {
            "valid": False,
            "message": "Certificate not found."
        }

    try:
        certificate_data = json.loads(
            certificate["certificate_data"]
        )

        data_string = json.dumps(
            certificate_data,
            sort_keys=True
        )

        calculated_hash = hashlib.sha256(
            data_string.encode("utf-8")
        ).hexdigest()

        stored_hash = certificate["record_hash"]

        if calculated_hash == stored_hash:
            return {
                "valid": True,
                "message":
                    "VERIFIED — Certificate record is intact.",
                "certificate":
                    certificate,
                "calculated_hash":
                    calculated_hash,
                "stored_hash":
                    stored_hash
            }

        return {
            "valid": False,
            "message":
                "ALTERED / INVALID — Hash mismatch detected.",
            "certificate":
                certificate,
            "calculated_hash":
                    calculated_hash,
            "stored_hash":
                    stored_hash
        }

    except Exception as error:

        return {
            "valid": False,
            "message":
                f"Verification error: {error}"
        }


def get_qr_file(certificate_number):
    """
    Return the QR image path if it exists.
    """

    qr_file = (
        QR_FOLDER /
        f"{certificate_number}.png"
    )

    if qr_file.exists():
        return str(qr_file)

    return None