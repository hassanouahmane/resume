from sqlalchemy.orm import Session
from ..models.user import User
from ..core.security import get_password_hash, verify_password, create_access_token
from typing import Optional


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, email: str, username: str, password: str, full_name: str | None = None) -> User:
    hashed = get_password_hash(password)
    user = User(email=email, username=username, full_name=full_name, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username_or_email) or get_user_by_email(db, username_or_email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_tokens_for_user(user: User) -> dict:
    access = create_access_token(str(user.id))
    return {"access_token": access, "token_type": "bearer"}
