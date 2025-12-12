from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from ...schemas.auth import UserCreate, UserOut, Token, ChangePassword
from ...core.database import get_db, engine
from ...models.user import User
from ...services.auth_service import (
    create_user,
    authenticate_user,
    create_tokens_for_user,
    get_user_by_email,
)
from ...core.security import decode_token, get_password_hash, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    user = create_user(db, payload.email, payload.username, payload.password, payload.full_name)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    tokens = create_tokens_for_user(user)
    return tokens


@router.get("/me", response_model=UserOut)
def me(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/refresh")
def refresh():
    # Placeholder for refresh token flow
    return {"detail": "Refresh token flow not implemented (stateless demo)"}


@router.post("/logout")
def logout():
    return {"detail": "Logged out (stateless token)"}


@router.post("/change-password")
def change_password(payload: ChangePassword, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    payload_token = decode_token(token)
    if not payload_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload_token.get("sub"))
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(payload.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password incorrect")
    user.hashed_password = get_password_hash(payload.new_password)
    db.add(user)
    db.commit()
    return {"detail": "Password changed"}
