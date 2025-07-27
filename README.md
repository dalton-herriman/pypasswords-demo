# How to securely store passwords in a database
This repository demonstrates how to securely implement password functionality with a database in Python.  
It is designed to be easy to follow, well-documented, and practical for beginners and intermediate developers.
###### *Example implementation written in Python*
---
## ✅ Features

- **Hashing**
    - via [Argon2id](https://argon2.online/) (industry standard, memory-hard).
- **Salting**
    - Support for an optional **pepper** stored outside the database (default implementation uses the local .env file)
- **Rate limiting**
    - Prevents brute force attacks
    - Configurable lockout mechanism
    - Database tie-in enables persistence across restarts
- **Password policy enforcement**:
  - Minimum length, special characters and specific string attributes
  - Entropy check with [zxcvbn](https://github.com/dwolfhub/zxcvbn-python) for password strength.
  - Check against known breaches via the [HaveIBeenPwned](https://haveibeenpwned.com/) API.
- **Field-level encryption support**
    - For extra security (optional)


---

## 📂 Project Structure
```plaintext
project/
│
├── app.py # Entry point (CLI menu)
├── config.py # Loads environment variables
├── password_service.py # Argon2id hashing + pepper
├── password_policy.py # Strength & breach checks
├── encryption.py # Optional Fernet encryption for DB fields
│
├── models/
│ └── user.py # User business logic
│
├── db/
│ ├── init.py
│ └── database.py # Database abstraction
│
└── cli/
├── register.py # Registration flow
└── login.py # Login flow
```
---
## 🚀 Getting Started
### 1️⃣ Clone and install
```bash
git clone https://github.com/dalton-herriman/pypasswords-demo.git
cd secure-password-tutorial
pip install -r requirements.txt
```

### 2️⃣ Create a .env file:
```env
DB_PATH=users.db
MAX_ATTEMPTS=5
LOCKOUT_TIME=30
APP_PEPPER=SomeSuperSecretRandomValue
FERNET_KEY=GENERATED_FERNET_KEY   # optional if using field encryption
```

### 3️⃣ Run the app:
```bash
python app.py
```
- Option 1
    - Register a new user (with password policy checks)
- Option 2
  - Login (rate limiting enforced)

---
## 📌 Security Principles Demonstrated
- Never store plaintext passwords – use one-way Argon2id hashing.

- Salting and Peppering – salts are automatic with Argon2; pepper adds another layer.

- Defense-in-depth – optional encryption of stored hashes adds another barrier.

- Rate limiting – protects against online brute-force attacks.

- Password policy enforcement – ensures strong, uncompromised passwords.

- Environment-based secrets – keep sensitive values out of source control.
---

## 🔒 Optional Enhancements
- ✅ Full database encryption with SQLCipher.
- ✅ Automatic password rehashing when Argon2 parameters change.
- ✅ Password reset flow with enforced policy.
- ✅ IP-based login attempt tracking.
- ✅ Integration with web frameworks (Flask/Django).

---
## 📚 Learning Goals
#### This project is meant to teach:

- How to properly hash passwords with Argon2id.

- How to store and verify passwords securely.

- How to enforce password strength and protect against weak credentials.

- How to mitigate brute-force attacks with rate limiting.

- How to separate concerns between user logic, DB access, and hashing services.

---
## 🤝 Contributing
**Pull requests and improvements welcome!**
*This repo is designed as a tutorial resource, so code clarity is prioritized over advanced abstractions.*