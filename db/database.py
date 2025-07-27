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
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.fetchall()
    
    def create_db(self):
        if not os.path.exists(self.db_path):
            self.connect()
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
