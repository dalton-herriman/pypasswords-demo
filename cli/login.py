from getpass import getpass
from password_service import PasswordService
from db.database import Database
from models.user import User
from config import DB_PATH

def login():
    db = Database(DB_PATH)
    password_service = PasswordService()

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    user = User(username, password, password_service)

    if user.verify(db):
        print("✅ Login successful.")
    else:
        print("❌ Invalid username or password.")
