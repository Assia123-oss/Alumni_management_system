from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from users.services import get_current_user
from users.schemas import User  # Add this import
from . import schemas, services

router = APIRouter()
event_service = services.EventService

@router.post("/", response_model=schemas.Event)
async def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # if not current_user.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Only administrators can create events"
    #     )
    return event_service(db).create(event)

@router.get("/", response_model=List[schemas.Event])
async def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return event_service(db).get_all(skip=skip, limit=limit)

@router.get("/{event_id}", response_model=schemas.Event)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = event_service(db).get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/{event_id}/register", response_model=schemas.EventRegistration)
async def register_for_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    event = event_service(db).get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    try:
        return event_service(db).register_participant(event_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{event_id}/participants", response_model=List[User])  # Changed from schemas.User to User
async def get_event_participants(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can view participant lists"
        )
    return event_service(db).get_participants(event_id)