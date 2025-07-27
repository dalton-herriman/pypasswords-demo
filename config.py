import os
from dotenv import load_dotenv

load_dotenv()

MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", 5))
LOCKOUT_TIME = int(os.getenv("LOCKOUT_TIME", 30))
DB_PATH = os.getenv("DB_PATH", "users.db")

APP_PEPPER = os.getenv("APP_PEPPER", "")
