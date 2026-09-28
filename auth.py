import hashlib
from database import get_connection


def hash_password(password):
    """Convert password into a SHA-256 hash."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(full_name, username, password, role):
    """Create a new user."""

    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute("""
            INSERT INTO users
            (full_name, username, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (
            full_name,
            username,
            password_hash,
            role
        ))

        connection.commit()
        return True, "User created successfully."

    except Exception as error:
        return False, str(error)

    finally:
        connection.close()


def authenticate_user(username, password):
    """Verify username and password."""

    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    cursor.execute("""
        SELECT id, full_name, username, role
        FROM users
        WHERE username = ?
        AND password_hash = ?
    """, (
        username,
        password_hash
    ))

    user = cursor.fetchone()

    connection.close()

    if user:
        return dict(user)

    return None


def get_all_users():
    """Return all registered users."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, full_name, username, role, created_at
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    connection.close()

    return [dict(user) for user in users]