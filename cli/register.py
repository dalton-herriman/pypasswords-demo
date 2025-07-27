from getpass import getpass
from password_policy import check_strength, check_breached
from password_service import PasswordService
from db.database import Database
from models.user import User
from config import DB_PATH


def register():
    db = Database(DB_PATH)
    password_service = PasswordService()

    db.create_db()
    db.setup_users_table()

    while True:
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        ok, msg = check_strength(password)
        if not ok:
            print(f"❌ {msg}\n")
            continue

        ok, msg = check_breached(password)
        if not ok:
            print(f"❌ {msg}\n")
            continue

        user = User(username, password, password_service)

        if user.save(db):
            print("✅ User created successfully.")
            break
        else:
            print(f"❌ Username '{username}' already exists. Please choose another.\n")
