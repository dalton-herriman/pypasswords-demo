import time
import os
from dotenv import load_dotenv
from password_service import PasswordService
from db.database import Database
from getpass import getpass

load_dotenv()

MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", 5))
LOCKOUT_TIME = int(os.getenv("LOCKOUT_TIME", 30))
DB_PATH = os.getenv("DB_PATH", "users.db")

class User:
    def __init__(self, username, password, password_service: PasswordService):
        self.username = username
        self.password = password
        self.password_service = password_service

    def save(self, db):
        hashed_password = self.password_service.hash_password(self.password)
        return db.add_user(self.username, hashed_password)
    
    def verify(self, db):
        failed_attempts, last_attempt = db.get_user_attempts(self.username)

        if failed_attempts >= MAX_ATTEMPTS and (time.time() - last_attempt) < LOCKOUT_TIME:
            remaining = int(LOCKOUT_TIME - (time.time() - last_attempt))
            print(f"Too many failed attempts. Try again in {remaining} seconds.")
            return False

        stored_hash = db.get_password_hash(self.username)
        if not stored_hash:
            self._register_failure(db, failed_attempts)
            return False

        if self.password_service.verify_password(stored_hash, self.password):
            db.reset_user_attempts(self.username)
            return True
        else:
            self._register_failure(db, failed_attempts)
            return False

    def _register_failure(self, db, current_attempts):
        db.update_user_attempts(self.username, current_attempts + 1, time.time())

def main():
    db = Database(DB_PATH)
    password_service = PasswordService()

    db.create_db()
    db.setup_users_table()

    while True:
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        user = User(username, password, password_service)

        if user.save(db):
            print("User created successfully.")
            break
        else:
            print(f"Username '{username}' already exists. Please choose a different one.\n")

    verify_pass = getpass("Re-enter password to verify: ")
    user_verify = User(username, verify_pass, password_service)

    if user_verify.verify(db):
        print("Password verified successfully.")
    else:
        print("Invalid username or password.")

if __name__ == "__main__":
    main()
