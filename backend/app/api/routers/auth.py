# app/api/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services import auth_service
from app.core.security import create_access_token, create_refresh_token
from app.api.deps import get_current_user   
from app.models.user import User 
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(
            db, payload.email, payload.password, payload.full_name
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"id": str(user.id), "email": user.email}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "full_name": current_user.full_name}