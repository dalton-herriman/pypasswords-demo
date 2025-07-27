import requests
from zxcvbn import zxcvbn
import hashlib

MIN_LENGTH = 12

def check_strength(password: str):
    if len(password) < MIN_LENGTH:
        return False, f"Password must be at least {MIN_LENGTH} characters."

    score = zxcvbn(password)['score']  # 0–4
    if score < 3:
        return False, "Password is too weak. Use more complexity or a longer passphrase."

    return True, "Password strength acceptable."

def check_breached(password: str):
    # k-Anonymity with HIBP API
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url, timeout=5)

    if res.status_code != 200:
        return True, "Could not check password breach status."

    hashes = (line.split(':') for line in res.text.splitlines())
    if any(h == suffix for h, count in hashes):
        return False, "This password appears in known breaches. Choose a different one."

    return True, "Password not found in breach list."
