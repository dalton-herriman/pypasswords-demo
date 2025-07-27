import time
from config import MAX_ATTEMPTS, LOCKOUT_TIME


class User:
    def __init__(self, username, password, password_service):
        self.username = username
        self.password = password
        self.password_service = password_service

    def save(self, db):
        hashed_password = self.password_service.hash_password(self.password)
        return db.add_user(self.username, hashed_password)

    def verify(self, db):
        failed_attempts, last_attempt = db.get_user_attempts(self.username)

        if (
            failed_attempts >= MAX_ATTEMPTS
            and (time.time() - last_attempt) < LOCKOUT_TIME
        ):
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
