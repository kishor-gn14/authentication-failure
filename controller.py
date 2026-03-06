from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from models import RegisterRequest, LoginRequest
import service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/unsecured/register")
def unsafe_register(request: RegisterRequest, db: Session = Depends(get_db)):

    if not request.username or not request.username.strip():
        return JSONResponse(status_code=400, content={
            "message": "Please enter a username."
        })

    if not request.password:
        return JSONResponse(status_code=400, content={
            "message": "Please enter a password."
        })

    result = service.register_user_weak(db, request)

    if not result["success"]:
        status = 409 if result.get("reason") == "conflict" else 400
        return JSONResponse(status_code=status, content={
            "message": result["message"]
        })

    return JSONResponse(status_code=201, content={
        "message":      result["message"],
        "securityNote": "No password policy applied. Password stored as plain text."
    })


@router.post("/unsecured/login")
def unsafe_login(request: LoginRequest, db: Session = Depends(get_db)):

    if not request.username or not request.username.strip():
        return JSONResponse(status_code=400, content={
            "message": "Please enter your username."
        })

    if not request.password:
        return JSONResponse(status_code=400, content={
            "message": "Please enter your password."
        })

    result = service.login_user_unsafe(db, request)

    if not result["success"]:
        status = 404 if result.get("reason") == "not_found" else 401
        return JSONResponse(status_code=status, content={
            "message":      result["message"],
            "securityNote": "No limit on login attempts. Password compared as plain text."
        })

    return JSONResponse(status_code=200, content={
        "message":      result["message"],
        "userId":       result["userId"],
        "role":         result["role"],
        "securityNote": "Login successful. Password was compared as plain text."
    })

@router.post("/secured/register")
def safe_register(request: RegisterRequest, db: Session = Depends(get_db)):

    if not request.username or not request.username.strip():
        return JSONResponse(status_code=400, content={
            "message": "Please enter a username."
        })

    if not request.password:
        return JSONResponse(status_code=400, content={
            "message": "Please enter a password."
        })

    result = service.register_user_strong(db, request)

    if not result["success"]:
        status = 409 if result.get("reason") == "conflict" else 400
        return JSONResponse(status_code=status, content={
            "message": result["message"]
        })

    return JSONResponse(status_code=201, content={
        "message":      result["message"],
        "securityNote": "Password policy enforced. Password stored as bcrypt hash."
    })

@router.post("/secured/login")
def safe_login(request: LoginRequest, db: Session = Depends(get_db)):

    if not request.username or not request.username.strip():
        return JSONResponse(status_code=400, content={
            "message": "Please enter your username."
        })

    if not request.password:
        return JSONResponse(status_code=400, content={
            "message": "Please enter your password."
        })

    result = service.login_user_safe(db, request)

    if not result["success"]:
        if result.get("reason") == "not_found":
            status = 404
        elif result.get("reason") == "account_locked":
            status = 423
        else:
            status = 401
        return JSONResponse(status_code=status, content={
            "message":      result["message"],
            "securityNote": result.get("securityNote", "")
        })

    return JSONResponse(status_code=200, content={
        "message":      result["message"],
        "userId":       result["userId"],
        "role":         result["role"],
        "securityNote": "bcrypt verification passed. Failed attempt counter reset."
    })