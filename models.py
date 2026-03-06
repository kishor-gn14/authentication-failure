from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel
from database import Base
from datetime import datetime

class UserTable(Base):
    __tablename__ = "users"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username         = Column(String,  unique=True, nullable=False)

    plain_password   = Column(String,  nullable=True)

    hashed_password  = Column(String,  nullable=True)

    role             = Column(String,  nullable=False, default="ROLE_USER")

class LoginAttemptTable(Base):
    __tablename__ = "login_attempts"

    id               = Column(Integer,  primary_key=True, index=True, autoincrement=True)
    username         = Column(String,   unique=True,  nullable=False)
    failed_count     = Column(Integer,  default=0,    nullable=False)
    is_locked        = Column(Boolean,  default=False,nullable=False)
    last_attempt_at  = Column(DateTime, nullable=True)

class RegisterRequest(BaseModel):
    username: str
    password: str
    role:     str = "ROLE_USER"

class LoginRequest(BaseModel):
    username: str
    password: str