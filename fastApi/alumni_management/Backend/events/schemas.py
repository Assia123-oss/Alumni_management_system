from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class EventBase(BaseModel):
    title: str
    description: str
    date: datetime
    location: str
    max_participants: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime
    current_participants: int = 0

    class Config:
        from_attributes = True

class EventRegistration(BaseModel):
    event_id: int
    user_id: int
    registration_date: datetime = datetime.now()

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None