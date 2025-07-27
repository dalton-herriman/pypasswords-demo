import os
from cryptography.fernet import Fernet
from config import FERNET_KEY

if FERNET_KEY is None:
    raise ValueError("FERNET_KEY must not be None")
key_bytes = FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY
cipher = Fernet(key_bytes)

def encrypt_value(value: str) -> bytes:
    return cipher.encrypt(value.encode())

def decrypt_value(token: bytes) -> str:
    return cipher.decrypt(token).decode()
