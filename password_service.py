import os
from argon2 import PasswordHasher, exceptions
from config import APP_PEPPER

class PasswordService:
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self.ph.hash(password + APP_PEPPER)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        try:
            self.ph.verify(hashed_password, password + APP_PEPPER)
            return True
        except exceptions.VerifyMismatchError:
            return False
