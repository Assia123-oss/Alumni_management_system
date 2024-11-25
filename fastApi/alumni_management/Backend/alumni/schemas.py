from pydantic import BaseModel
from typing import Optional
from datetime import date

class AlumniBase(BaseModel):
    graduation_year: int
    degree: str
    major: str
    current_job: Optional[str] = None
    company: Optional[str] = None

class AlumniCreate(AlumniBase):
    pass

class AlumniUpdate(BaseModel):
    graduation_year: Optional[int] = None
    degree: Optional[str] = None
    major: Optional[str] = None
    current_job: Optional[str] = None
    company: Optional[str] = None

class Alumni(AlumniBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True