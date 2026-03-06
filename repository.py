from sqlalchemy.orm import Session
from models import UserTable, LoginAttemptTable
from datetime import datetime

def username_exists(db: Session, username: str) -> bool:
    return db.query(UserTable).filter(
        UserTable.username == username
    ).first() is not None


def create_user(db: Session, username: str, plain_password: str,
                hashed_password: str, role: str) -> UserTable:
    new_user = UserTable(
        username        = username,
        plain_password  = plain_password,
        hashed_password = hashed_password,
        role            = role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str) -> UserTable | None:
    return db.query(UserTable).filter(
        UserTable.username == username
    ).first()

def get_login_attempt(db: Session, username: str) -> LoginAttemptTable | None:
    return db.query(LoginAttemptTable).filter(
        LoginAttemptTable.username == username
    ).first()


def increment_failed_attempt(db: Session, username: str) -> LoginAttemptTable:
    LOCKOUT_THRESHOLD = 2

    attempt = get_login_attempt(db, username)

    if attempt is None:
        attempt = LoginAttemptTable(
            username        = username,
            failed_count    = 1,
            is_locked       = False,
            last_attempt_at = datetime.utcnow()
        )
        db.add(attempt)
    else:
        attempt.failed_count    += 1
        attempt.last_attempt_at  = datetime.utcnow()

        if attempt.failed_count >= LOCKOUT_THRESHOLD:
            attempt.is_locked = True

    db.commit()
    db.refresh(attempt)
    return attempt


def reset_failed_attempts(db: Session, username: str) -> None:
    attempt = get_login_attempt(db, username)
    if attempt:
        attempt.failed_count = 0
        attempt.is_locked    = False
        db.commit()