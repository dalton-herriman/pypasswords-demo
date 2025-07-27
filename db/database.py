import os
import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=()):
        if self.connection is None:
            self.connect()
        if self.connection is None:
            raise RuntimeError("Database connection could not be established.")
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.fetchall()
    
    def create_db(self):
        if not os.path.exists(self.db_path):
            self.connect()
            if self.connection is not None:
                self.connection.close()

    def setup_users_table(self):
        self.connect()
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
        self.execute_query(query)

        columns = self.execute_query("PRAGMA table_info(users)")
        col_names = [c[1] for c in columns]

        if "failed_attempts" not in col_names:
            self.execute_query("ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0")
        if "last_attempt" not in col_names:
            self.execute_query("ALTER TABLE users ADD COLUMN last_attempt REAL DEFAULT 0")

        self.close()
        
    def get_user_attempts(self, username):
        self.connect()
        query = "SELECT failed_attempts, last_attempt FROM users WHERE username = ?"
        result = self.execute_query(query, (username,))
        self.close()
        return result[0] if result else (0, 0)

    def update_user_attempts(self, username, attempts, timestamp):
        self.connect()
        query = "UPDATE users SET failed_attempts = ?, last_attempt = ? WHERE username = ?"
        self.execute_query(query, (attempts, timestamp, username))
        self.close()

    def reset_user_attempts(self, username):
        self.connect()
        query = "UPDATE users SET failed_attempts = 0, last_attempt = 0 WHERE username = ?"
        self.execute_query(query, (username,))
        self.close()
    
    def add_user(self, username, hashed_password):
        self.connect()
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        try:
            self.execute_query(query, (username, hashed_password))
        except sqlite3.IntegrityError:
            self.close()
            return False
        self.close()
        return True

    def get_password_hash(self, username):
        self.connect()
        query = "SELECT password FROM users WHERE username = ?"
        result = self.execute_query(query, (username,))
        self.close()
        return result[0][0] if result else None
