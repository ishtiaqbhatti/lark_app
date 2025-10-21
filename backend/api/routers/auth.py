from fastapi import APIRouter, HTTPException
from ..models import LoginRequest

router = APIRouter()


@router.post("/auth/login")
async def login(request: LoginRequest):
    """
    Dummy login endpoint for development.
    In a real app, verify a hashed password against a user database.
    """
    DUMMY_PASSWORD = "password123"
    if request.password == DUMMY_PASSWORD:
        dummy_user = {"username": "admin", "email": "admin@example.com"}
        dummy_token = "dummy-secret-token"
        return {"user": dummy_user, "token": dummy_token}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")


@router.post("/auth/logout")
async def logout():
    """Dummy logout endpoint."""
    return {"message": "Logged out successfully"}
