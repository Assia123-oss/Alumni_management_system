from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from users.services import get_current_user
from users.models import User
from . import schemas, services

router = APIRouter(tags=["alumni"])

@router.post("/", response_model=schemas.Alumni)
async def create_alumni(
    alumni: schemas.AlumniCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create alumni profile for current user"""
    # Check if alumni profile already exists
    existing_alumni = services.AlumniService(db).get_by_user_id(current_user.id)
    if existing_alumni:
        raise HTTPException(
            status_code=400,
            detail="Alumni profile already exists for this user"
        )
    return services.AlumniService(db).create(current_user.id, alumni)

@router.get("/me", response_model=schemas.Alumni)
async def read_my_alumni(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's alumni profile"""
    alumni = services.AlumniService(db).get_by_user_id(current_user.id)
    if not alumni:
        raise HTTPException(status_code=404, detail="Alumni profile not found")
    return alumni

@router.get("/", response_model=List[schemas.Alumni])
async def read_alumni(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all alumni profiles"""
    return services.AlumniService(db).get_all(skip=skip, limit=limit)

@router.put("/{alumni_id}", response_model=schemas.Alumni)
async def update_alumni(
    alumni_id: int,
    alumni: schemas.AlumniUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an alumni profile"""
    db_alumni = services.AlumniService(db).get_by_id(alumni_id)
    if not db_alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    if db_alumni.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")
    return services.AlumniService(db).update(alumni_id, alumni)

@router.delete("/{alumni_id}")
async def delete_alumni(
    alumni_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an alumni profile"""
    db_alumni = services.AlumniService(db).get_by_id(alumni_id)
    if not db_alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    if db_alumni.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this profile")
    return services.AlumniService(db).delete(alumni_id)