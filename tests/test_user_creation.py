from app import User

def test_user_creation_and_verification(temp_db, password_service):
    user = User("testuser", "securepassword", password_service)
    assert user.save(temp_db), "User should be created successfully"
    assert user.verify(temp_db), "Password verification should succeed"

def test_duplicate_user(temp_db, password_service):
    user1 = User("testuser", "password1", password_service)
    user2 = User("testuser", "password2", password_service)
    assert user1.save(temp_db), "First user creation should succeed"
    assert not user2.save(temp_db), "Duplicate username should fail"
