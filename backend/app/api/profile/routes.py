from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import Optional
from ...models.user import User
from ...schemas.auth import UserOut, UserCreate
from ...core.database import get_db
from ...core.dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


# -------------------------
# Get current user's profile
# -------------------------
@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


# -------------------------
# Get user by ID (JSON body)
# -------------------------
@router.post("/get", response_model=UserOut)
def get_user(
    user_id: Optional[int] = Body(..., embed=True),  # require JSON body like {"user_id": 1}
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------------------------
# Update current user's profile
# -------------------------
@router.put("/me", response_model=UserOut)
def update_my_profile(
    payload: UserCreate,  # reuse existing schema for email, username, full_name
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.email:
        current_user.email = payload.email
    if payload.username:
        current_user.username = payload.username
    if payload.full_name:
        current_user.full_name = payload.full_name

    db.commit()
    db.refresh(current_user)
    return current_user


# -------------------------
# Delete current user's account
# -------------------------
@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(current_user)
    db.commit()
    return {"detail": "Account deleted successfully"}
