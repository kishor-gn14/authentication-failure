Authentication failures occur when applications do not properly verify user identity or protect login mechanisms. These weaknesses may allow attackers to guess passwords, bypass authentication, or gain unauthorized access to user accounts.

This lab allows learners to:

1. Discover authentication weaknesses  
2. Exploit insecure login mechanisms  
3. Implement secure authentication protections  

---

# Vulnerability Selected and Why It Matters

Authentication systems are the **first line of defense** in most applications. If authentication is implemented incorrectly, attackers may gain unauthorized access to accounts and sensitive data.

Common authentication mistakes include:

- Storing passwords in **plain text**
- Allowing **weak passwords**
- Not limiting **login attempts**
- Missing **account lock mechanisms**

These weaknesses can lead to **brute-force attacks, credential theft, and account compromise**.

This lab demonstrates how these vulnerabilities occur and how secure practices can prevent them.

---

# Target Audience

This lab is designed for:

- Developers learning **secure coding practices**
- Students studying **application security**
- Beginners exploring **OWASP vulnerabilities**

---

# Learning Objectives

After completing this lab learners will be able to:

- Understand how authentication failures occur in web applications
- Identify insecure authentication implementations
- Demonstrate how unlimited login attempts allow brute-force attacks
- Implement secure password storage using **bcrypt hashing**
- Apply protections such as **password policies and account lock mechanisms**

---

# Lab Scenario (Discover → Exploit → Fix)

The application contains **two versions of authentication APIs**:

- **Unsecured authentication API** (vulnerable)
- **Secured authentication API** (fixed implementation)

### Step 1 — Discover the Vulnerability

Learners interact with vulnerable endpoints:

POST /api/auth/unsecured/register  
POST /api/auth/unsecured/login

Problems in this version:

- Passwords stored as **plain text**
- Weak passwords accepted
- Unlimited login attempts
- No account lock protection

Learners observe that weak passwords are accepted and repeated login attempts are allowed.

---

### Step 2 — Exploit the Vulnerability

Attackers can attempt multiple login attempts using the unsecured endpoint.

Example request:

POST http://localhost:8000/api/auth/unsecured/login

```json
{
 "username": "kishor",
 "password": "welcome1"
}
```

Because there is **no limit on login attempts**, attackers can repeatedly try passwords until they succeed.

This demonstrates how **brute-force attacks** exploit weak authentication systems.

---

### Step 3 — Fix the Vulnerability

The secured version of the API introduces stronger authentication controls.

Secure endpoints:

POST /api/auth/secured/register  
POST /api/auth/secured/login  

Security improvements include:

- Password hashing using **bcrypt**
- Password strength validation
- Failed login attempt tracking
- Automatic account lock after multiple failures

Learners can compare the vulnerable and secure implementations to understand how authentication vulnerabilities can be prevented.

---

# Technical Design

## Architecture

```
Client (Postman)
        │
        ▼
FastAPI Controller Layer
        │
        ▼
Service Layer (Authentication Logic)
        │
        ▼
Repository Layer
        │
        ▼
SQLite Database
```

---

## Technology Stack

| Component | Technology |
|---|---|
Language | Python |
Framework | FastAPI |
Database | SQLite |
ORM | SQLAlchemy |
Security | bcrypt |

---

# Running the Lab

### 1 Install dependencies

```
pip install -r requirements.txt
```

### 2 Start the server

```
uvicorn main:app --reload
```

### 3 Open API documentation

```
http://localhost:8000/docs
```

The Swagger UI allows learners to test both **vulnerable and secure authentication APIs**.

---

# Lab Demonstration

## Vulnerable Registration

POST http://localhost:8000/api/auth/unsecured/register

```json
{
  "username": "kishor",
  "password": "123",
  "role": "Billing"
}
```

Weak passwords are accepted.

---

## Secure Registration (Weak Password Rejected)

POST http://localhost:8000/api/auth/secured/register

```json
{
  "username": "rishi",
  "password": "123",
  "role": "Billing"
}
```

Password policy rejects weak passwords.

---

## Secure Registration (Strong Password)

POST http://localhost:8000/api/auth/secured/register

```json
{
  "username": "rishi",
  "password": "Rishi@123",
  "role": "Billing"
}
```

Password is securely stored using bcrypt hashing.

---

## Unsecured Login (Unlimited Attempts)

POST http://localhost:8000/api/auth/unsecured/login

```json
{
  "username": "kishor",
  "password": "welcome1"
}
```

```json
{
  "username": "kishor",
  "password": "welcome2"
}
```

The system allows unlimited attempts, demonstrating the risk of brute-force attacks.

---

## Secure Login

POST http://localhost:8000/api/auth/secured/login

```json
{
  "username": "rishi",
  "password": "Rishi@123"
}
```

Authentication succeeds using **bcrypt password verification**.

---

# Learning Validation

Learners validate their understanding by completing the following tasks:

1. Register a user using the **unsecured API**
2. Attempt multiple incorrect login attempts
3. Observe that unlimited attempts are allowed
4. Register a user using the **secured API**
5. Trigger account lock after repeated login failures
6. Successfully log in using the secure authentication endpoint

Completion of these tasks demonstrates understanding of authentication vulnerabilities and secure implementations.

---

# Repository Structure

| File | Description |
|---|---|
controller.py | API endpoints |
service.py | Authentication logic |
repository.py | Database operations |
models.py | Database models |
database.py | Database configuration |
main.py | Application entry point |

---


