from database import get_connection


def register_instrument(
    instrument_number,
    instrument_type,
    manufacturer,
    model,
    capacity,
    owner_name,
    location
):
    """Register a new weighing/measuring instrument."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO instruments (
                instrument_number,
                instrument_type,
                manufacturer,
                model,
                capacity,
                owner_name,
                location
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            instrument_number,
            instrument_type,
            manufacturer,
            model,
            capacity,
            owner_name,
            location
        ))

        connection.commit()

        return True, "Instrument registered successfully."

    except Exception as error:

        return False, str(error)

    finally:

        connection.close()


def get_user_instruments(owner_name):
    """Get instruments belonging to a user."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM instruments
        WHERE owner_name = ?
        ORDER BY id DESC
    """, (owner_name,))

    instruments = cursor.fetchall()

    connection.close()

    return [dict(instrument) for instrument in instruments]


def get_all_instruments():
    """Get all registered instruments."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM instruments
        ORDER BY id DESC
    """)

    instruments = cursor.fetchall()

    connection.close()

    return [dict(instrument) for instrument in instruments]