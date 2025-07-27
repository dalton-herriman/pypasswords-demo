from password_service import PasswordService
from db.database import Database
from getpass import getpass

class User:
    def __init__(self, username, password, password_service: PasswordService):
        self.username = username
        self.password = password
        self.password_service = password_service

    def save(self, db):
        hashed_password = self.password_service.hash_password(self.password)
        return db.add_user(self.username, hashed_password)
    
    def verify(self, db):
        stored_hash = db.get_password_hash(self.username)
        if not stored_hash:
            return False
        return self.password_service.verify_password(stored_hash, self.password)

def main():
    db = Database('users.db')
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
