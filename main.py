from fastapi import FastAPI
from database import Base, engine
from controller import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication Failures",
    description="OWASP A07:2025 — Hands-on security lab using FastAPI and SQLite",
    version="1.0.0"
)

app.include_router(router)