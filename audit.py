import sqlite3
from datetime import datetime

DB_NAME = "data/measure_verify.db"


def log_action(
    username,
    action,
    entity_type=None,
    entity_id=None,
    details=None
):
    """
    Store an action in the audit log.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO audit_logs
        (
            username,
            action,
            entity_type,
            entity_id,
            timestamp,
            details
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        username,
        action,
        entity_type,
        entity_id,
        timestamp,
        details
    ))

    conn.commit()
    conn.close()


def get_audit_logs(limit=100):
    """
    Retrieve recent audit log entries.
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            action,
            entity_type,
            entity_id,
            timestamp,
            details
        FROM audit_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    logs = cursor.fetchall()

    conn.close()

    return logs