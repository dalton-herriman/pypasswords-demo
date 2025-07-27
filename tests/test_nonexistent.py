from app import User

def test_nonexistent_user(temp_db, password_service):
    user = User("nouser", "password", password_service)
    assert not user.verify(temp_db), "Verification for non-existent user should fail"
