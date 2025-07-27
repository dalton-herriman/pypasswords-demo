from argon2 import PasswordHasher, exceptions
import os

PEPPER = os.getenv("APP_PEPPER", "SomeVerySecretRandomKey")
class PasswordService:
    def __init__(self):
        self.ph = PasswordHasher()  # Uses Argon2id by default

    def hash_password(self, password: str) -> str:
        return self.ph.hash(password + PEPPER)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        try:
            self.ph.verify(hashed_password, password + PEPPER)
            return True
        except exceptions.VerifyMismatchError:
            return False
