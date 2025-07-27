from argon2 import PasswordHasher, exceptions

class PasswordService:
    def __init__(self):
        self.ph = PasswordHasher()  # Uses Argon2id by default

    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        try:
            self.ph.verify(hashed_password, password)
            return True
        except exceptions.VerifyMismatchError:
            return False
