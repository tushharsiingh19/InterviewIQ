# app/services/auth_service.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token


def register_user(db: Session, email: str, password: str, full_name: str) -> User:
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ValueError("A user with this email already exists")

    new_user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user