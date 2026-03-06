import bcrypt
import repository
from models import RegisterRequest, LoginRequest
from sqlalchemy.orm import Session

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")
    salt           = bcrypt.gensalt()
    hashed         = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes   = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def is_password_strong(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password is too short. Use at least 8 characters."

    if not any(char.isdigit() for char in password):
        return False, "Password must include at least one number."

    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_characters for char in password):
        return False, "Password must include at least one special character (e.g. !, @, #)."

    return True, ""


def register_user_weak(db: Session, request: RegisterRequest) -> dict:
    if repository.username_exists(db, request.username):
        return {
            "success": False,
            "reason":  "conflict",
            "message": f"The username '{request.username}' is already taken. Please choose a different one."
        }

    repository.create_user(
        db,
        username        = request.username,
        plain_password  = request.password,
        hashed_password = hash_password(request.password),
        role            = request.role
    )

    return {
        "success": True,
        "message": "Account created successfully."
    }


def register_user_strong(db: Session, request: RegisterRequest) -> dict:
    if repository.username_exists(db, request.username):
        return {
            "success": False,
            "reason":  "conflict",
            "message": f"The username '{request.username}' is already taken. Please choose a different one."
        }

    is_strong, reason = is_password_strong(request.password)
    if not is_strong:
        return {
            "success": False,
            "reason":  "weak_password",
            "message": reason
        }

    repository.create_user(
        db,
        username        = request.username,
        plain_password  = None,
        hashed_password = hash_password(request.password),
        role            = request.role
    )

    return {
        "success": True,
        "message": "Account created successfully."
    }

def login_user_unsafe(db: Session, request: LoginRequest) -> dict:
    user = repository.get_user_by_username(db, request.username)

    if user is None:
        return {
            "success": False,
            "reason":  "not_found",
            "message": f"No account found for '{request.username}'. Please register first."
        }

    if request.password != user.plain_password:

        return {
            "success": False,
            "reason":  "invalid_credentials",
            "message": "Incorrect password. Please try again."
        }

    return {
        "success": True,
        "message": f"Welcome back, {user.username}!",
        "userId":  user.id,
        "role":    user.role
    }



def login_user_safe(db: Session, request: LoginRequest) -> dict:
    user = repository.get_user_by_username(db, request.username)

    if user is None:
        return {
            "success": False,
            "reason":  "not_found",
            "message": f"No account found for '{request.username}'. Please register first."
        }

    attempt_record = repository.get_login_attempt(db, request.username)
    if attempt_record and attempt_record.is_locked:
        return {
            "success": False,
            "reason":  "account_locked",
            "message": f"Your account has been locked after {attempt_record.failed_count} "
                       "failed login attempts. Please contact support to unlock it."
        }

    if not verify_password(request.password, user.hashed_password):

        updated_attempt = repository.increment_failed_attempt(db, request.username)
        remaining       = max(0, 1 - updated_attempt.failed_count)

        if updated_attempt.is_locked:
            return {
                "success": False,
                "reason":  "account_locked",
                "message": "Your account has been locked after 2 failed login attempts. "
                           "Please contact support to unlock it."
            }

        return {
            "success": False,
            "reason":  "invalid_credentials",
            "message": f"Incorrect password. You have {remaining} attempt(s) left before your account is locked."
        }

    repository.reset_failed_attempts(db, request.username)

    return {
        "success": True,
        "message": f"Welcome back, {user.username}!",
        "userId":  user.id,
        "role":    user.role
    }