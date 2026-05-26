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

