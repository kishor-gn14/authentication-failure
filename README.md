1. Vulnerability Selected and Why It Matters

This lab demonstrates Authentication Failures, which is one of the major risks listed in the OWASP Top 10.

Authentication failures occur when applications do not properly verify user identity or protect login mechanisms. Common issues include storing passwords insecurely, allowing weak passwords, and not limiting login attempts.

If authentication is poorly implemented, attackers may:

Gain unauthorized access to user accounts

Perform brute-force attacks to guess passwords

Access sensitive information

This lab focuses on demonstrating how weak authentication can be exploited and how secure practices such as password hashing and login attempt limits can prevent these attacks.

2. Target Audience and Learning Objectives
Target Audience

This lab is designed for:

Developers learning secure coding practices

Students studying application security

Beginners exploring common web security vulnerabilities

Learning Objectives

After completing this lab, learners will be able to:

Understand how authentication failures occur in web applications.

Identify insecure authentication implementations.

Demonstrate how unlimited login attempts can enable brute-force attacks.

Implement secure password storage using hashing.

Apply protections such as password policies and account lock mechanisms.

3. Lab Scenario (Discover → Exploit → Fix)

The lab contains two versions of authentication APIs: a vulnerable version and a secure version.

Step 1 – Discover the Vulnerability

Learners interact with the vulnerable authentication endpoints.

Example endpoints:

POST /api/auth/unsecured/register
POST /api/auth/unsecured/login

In this version:

Passwords are stored as plain text

Weak passwords are allowed

Login attempts are unlimited

Learners observe that the system accepts weak passwords and allows repeated login attempts.

Step 2 – Exploit the Vulnerability

Learners attempt multiple incorrect login attempts using the unsecured login endpoint.

Example request:

POST /api/auth/unsecured/login
{
 "username": "kishor",
 "password": "wrong1"
}

Because there is no login attempt limit, attackers can continue trying different passwords until they succeed.

This demonstrates how brute-force attacks can occur when authentication controls are weak.

Step 3 – Fix the Vulnerability

The secure version of the API introduces several protections.

Secure endpoints:

POST /api/auth/secured/register
POST /api/auth/secured/login

Security improvements include:

Password hashing using bcrypt

Password strength validation

Tracking failed login attempts

Automatic account lock after repeated failures

Learners can compare the behavior between the vulnerable and secure versions to understand how proper authentication controls prevent attacks.

4. Technical Design
Architecture

The application follows a layered architecture:

Client (Postman / Browser)
        │
FastAPI Controller Layer
        │
Service Layer (Authentication Logic)
        │
Repository Layer
        │
SQLite Database
Technology Stack

Language: Python
Framework: FastAPI
Database: SQLite
ORM: SQLAlchemy
Security Library: bcrypt

Deployment Approach

The application runs locally for safe experimentation.

Steps to run the lab:

Install dependencies

pip install -r requirements.txt

Start the server

uvicorn main:app --reload

Access API documentation

http://localhost:8000/docs

This allows learners to interact with the vulnerable and secure authentication endpoints.

5. Learning Validation

Learners validate their understanding by completing the following tasks.

Task 1

Register a user using the vulnerable API with a weak password.

Task 2

Attempt multiple incorrect login attempts and observe that the system allows unlimited attempts.

Task 3

Register a user using the secure API and observe password policy enforcement.

Task 4

Trigger account lock by exceeding the allowed number of failed login attempts.

Task 5

Successfully log in using the secure authentication endpoint.

Completion of these tasks confirms that learners understand the authentication vulnerability and the implemented security protections.

Prototype

A working prototype of the lab has been implemented using Python FastAPI with SQLite.

The prototype includes:

Vulnerable authentication endpoints

Secure authentication endpoints

Password hashing with bcrypt

Password policy validation

Login attempt tracking

Account lock mechanism

The application is intended for educational purposes only and demonstrates both insecure and secure authentication implementations.