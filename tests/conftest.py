# shared fixture for all tests
import os
import tempfile
import pytest
from db.database import Database
from password_service import PasswordService

@pytest.fixture
def temp_db():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    db_path = temp_file.name
    db = Database(db_path)
    db.create_db()
    db.setup_users_table()
    yield db
    db.close()
    os.remove(db_path)

@pytest.fixture
def password_service():
    return PasswordService()
