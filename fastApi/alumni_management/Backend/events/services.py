from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import List
from . import models, schemas
from users.models import User

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, event: schemas.EventCreate, user: User):
        """Create new event (admin only)"""
        if not user.is_admin:  # We'll need to add this field to User model
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create events"
            )
        
        db_event = models.Event(
            title=event.title,
            description=event.description,
            date=event.date,
            location=event.location,
            is_virtual=event.is_virtual,
            max_participants=event.max_participants,
            created_by=user.id
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_by_id(self, event_id: int):
        """Get event by ID"""
        return self.db.query(models.Event).filter(models.Event.id == event_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        """Get all events"""
        return self.db.query(models.Event).offset(skip).limit(limit).all()

    def update(self, event_id: int, event: schemas.EventUpdate, user: User):
        """Update event (admin only)"""
        db_event = self.get_by_id(event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can update events"
            )

        update_data = event.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)

        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def delete(self, event_id: int, user: User):
        """Delete event (admin only)"""
        db_event = self.get_by_id(event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can delete events"
            )

        self.db.delete(db_event)
        self.db.commit()
        return {"message": "Event deleted successfully"}

    def register_participant(self, event_id: int, user: User):
        """Register user for an event"""
        db_event = self.get_by_id(event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Check if event is full
        if db_event.max_participants:
            current_participants = self.db.query(models.EventRegistration).filter(
                models.EventRegistration.event_id == event_id
            ).count()
            if current_participants >= db_event.max_participants:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Event is already full"
                )

        # Check if user is already registered
        existing_registration = self.db.query(models.EventRegistration).filter(
            models.EventRegistration.event_id == event_id,
            models.EventRegistration.user_id == user.id
        ).first()
        
        if existing_registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already registered for this event"
            )

        # Create registration
        registration = models.EventRegistration(
            event_id=event_id,
            user_id=user.id
        )
        self.db.add(registration)
        self.db.commit()
        return {"message": "Successfully registered for event"}

    def unregister_participant(self, event_id: int, user: User):
        """Unregister user from an event"""
        registration = self.db.query(models.EventRegistration).filter(
            models.EventRegistration.event_id == event_id,
            models.EventRegistration.user_id == user.id
        ).first()
        
        if not registration:
            raise HTTPException(
                status_code=404,
                detail="You are not registered for this event"
            )

        self.db.delete(registration)
        self.db.commit()
        return {"message": "Successfully unregistered from event"}

    def get_participants(self, event_id: int, user: User):
        """Get list of participants for an event (admin only)"""
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can view participant lists"
            )

        return self.db.query(models.EventRegistration).filter(
            models.EventRegistration.event_id == event_id
        ).all()

    def get_user_events(self, user: User):
        """Get all events user is registered for"""
        return self.db.query(models.Event).join(
            models.EventRegistration
        ).filter(
            models.EventRegistration.user_id == user.id
        ).all()