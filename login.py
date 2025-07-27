'''
This script provides a CLI for testing login functionality during development.
Use automated tests to verify code; this script is not for production use.
'''
import os
from getpass import getpass
from dotenv import load_dotenv
from password_service import PasswordService
from db.database import Database
from app import User   # reusing the User class

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "users.db")

def login():
    db = Database(DB_PATH)
    password_service = PasswordService()

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    user = User(username, password, password_service)

    while not user.verify(db):
        print("❌ Invalid username or password.")
        username = input("Enter username: ")
        password = getpass("Enter password: ")
        user = User(username, password, password_service)
    print("✅ Login successful.")

if __name__ == "__main__":
    login()
