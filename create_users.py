from database import initialize_database
from auth import create_user


initialize_database()

users = [
    ("Demo User", "user", "user123", "User"),
    ("Demo LMO", "lmo", "lmo123", "LMO"),
    ("Demo GATC", "gatc", "gatc123", "GATC"),
    ("System Administrator", "admin", "admin123", "Admin")
]

for full_name, username, password, role in users:

    success, message = create_user(
        full_name,
        username,
        password,
        role
    )

    if success:
        print(f"{role} account created: {username}")
    else:
        print(f"{username}: {message}")

print("\nDemo users setup completed.")