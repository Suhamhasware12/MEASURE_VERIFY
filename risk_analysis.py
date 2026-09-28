import sqlite3
from datetime import datetime

DB_NAME = "data/measure_verify.db"


def calculate_risk(instrument_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get inspection history
    cursor.execute("""
        SELECT
            failure_count,
            result,
            inspection_date
        FROM inspections
        WHERE application_id IN (
            SELECT id
            FROM applications
            WHERE instrument_id = ?
        )
        ORDER BY id DESC
    """, (instrument_id,))

    inspections = cursor.fetchall()

    # Calculate failure count
    total_failures = 0

    for inspection in inspections:
        total_failures += inspection["failure_count"] or 0

    # Check whether the instrument has previous failed inspections
    failed_inspections = sum(
        1
        for inspection in inspections
        if inspection["result"] == "FAIL"
    )

    # Basic explainable risk scoring
    risk_score = 0
    explanations = []

    # Failure history
    if failed_inspections >= 3:
        risk_score += 50
        explanations.append(
            "Multiple previous inspection failures"
        )
    elif failed_inspections >= 1:
        risk_score += 25
        explanations.append(
            "Previous inspection failure detected"
        )

    # Failure count
    if total_failures >= 5:
        risk_score += 30
        explanations.append(
            "High cumulative failure count"
        )
    elif total_failures >= 2:
        risk_score += 15
        explanations.append(
            "Repeated failure observations"
        )

    # Determine risk level
    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if not explanations:
        explanations.append(
            "No significant abnormal verification pattern detected"
        )

    explanation = "; ".join(explanations)

    # Save/update risk record
    cursor.execute("""
        SELECT id
        FROM risk_records
        WHERE instrument_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (instrument_id,))

    existing_record = cursor.fetchone()

    analysis_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if existing_record:
        cursor.execute("""
            UPDATE risk_records
            SET risk_level = ?,
                risk_score = ?,
                failure_count = ?,
                abnormal_pattern_flag = ?,
                analysis_date = ?,
                explanation = ?
            WHERE id = ?
        """, (
            risk_level,
            risk_score,
            total_failures,
            1 if failed_inspections > 0 else 0,
            analysis_date,
            explanation,
            existing_record["id"]
        ))
    else:
        cursor.execute("""
            INSERT INTO risk_records
            (
                instrument_id,
                risk_level,
                risk_score,
                failure_count,
                overdue_flag,
                abnormal_pattern_flag,
                analysis_date,
                explanation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            instrument_id,
            risk_level,
            risk_score,
            total_failures,
            0,
            1 if failed_inspections > 0 else 0,
            analysis_date,
            explanation
        ))

    conn.commit()
    conn.close()

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "failure_count": total_failures,
        "explanation": explanation
    }


def get_instrument_risk(instrument_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            instrument_id,
            risk_level,
            risk_score,
            failure_count,
            overdue_flag,
            abnormal_pattern_flag,
            analysis_date,
            explanation
        FROM risk_records
        WHERE instrument_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (instrument_id,))

    risk = cursor.fetchone()

    conn.close()

    return risk


def get_all_risk_records():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.instrument_id,
            i.instrument_number,
            i.instrument_type,
            i.owner_name,
            i.location,
            r.risk_level,
            r.risk_score,
            r.failure_count,
            r.overdue_flag,
            r.abnormal_pattern_flag,
            r.analysis_date,
            r.explanation
        FROM risk_records r
        LEFT JOIN instruments i
            ON r.instrument_id = i.id
        ORDER BY
            CASE r.risk_level
                WHEN 'HIGH' THEN 1
                WHEN 'MEDIUM' THEN 2
                WHEN 'LOW' THEN 3
                ELSE 4
            END,
            r.risk_score DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records