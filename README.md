# 🔐 Cipher Safe — Encrypted Password Vault (Python + SQLite + AES)

A CLI-based secure password vault system built using Python that demonstrates real-world authentication, encryption, and secure data storage concepts.

---

# 🚀 Overview

Cipher Safe is a simple password manager where users can:
- Register securely
- Login with hashed passwords
- Store secrets securely
- Encrypt data using AES
- Decrypt data only after authentication

---


# ⚙️ How It Works

## 1️⃣ Registration
- Username + password input
- Password hashed using bcrypt
- Stored in SQLite database

---

## 2️⃣ Login
- Username verified from DB
- bcrypt checks password
- If correct → access granted

---

## 3️⃣ Vault System

### ➕ Add Data
- User enters title + secret
- Secret encrypted using AES (CBC mode)
- Encrypted data + IV stored in DB

---

### 🔓 View Data
- Encrypted data fetched
- AES decryption performed
- Original secret displayed

---

# 🔐 Security Used

- bcrypt password hashing
- AES encryption (CBC mode)
- Random IV per encryption
- Base64 encoding for DB storage
- SQLite structured storage

---

# 🧰 Tools & Libraries

- Python 3.x  
- sqlite3  
- bcrypt  
- pycryptodome (AES)  
- base64  

---

