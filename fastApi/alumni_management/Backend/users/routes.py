from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from app.core.security import create_access_token
from app.core.config import settings
from app.core.database import get_db
from . import schemas
from .services import UserService, get_current_user
from .models import User
from . import schemas, services, models

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    db_user = UserService(db).get_by_email(user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return UserService(db).create(user)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = UserService(db).authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Move /me endpoint BEFORE /{user_id}
@router.get("/me", response_model=schemas.User)
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """Get current logged in user"""
    return current_user

@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return UserService(db).get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    user = UserService(db).get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a user"""
    # Check if user exists
    db_user = UserService(db).get_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is updating their own profile
    # if current_user.id != user_id:
    #     raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    return UserService(db).update(user_id, user_update)

@router.put("/me/password", response_model=schemas.User)
async def change_password(
    password_update: schemas.UserPasswordUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's password"""
    user = services.UserService(db).change_password(
        current_user.id,
        password_update.current_password,
        password_update.new_password
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a user"""
    # Check if user exists
    db_user = UserService(db).get_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only allow users to delete their own account
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    return UserService(db).delete(user_id)