from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

class AlumniService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, alumni_id: int):
        return self.db.query(models.Alumni).filter(models.Alumni.id == alumni_id).first()

    def get_by_user_id(self, user_id: int):
        return self.db.query(models.Alumni).filter(models.Alumni.user_id == user_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Alumni).offset(skip).limit(limit).all()

    def create(self, user_id: int, alumni: schemas.AlumniCreate):
        db_alumni = models.Alumni(
            user_id=user_id,
            **alumni.model_dump()
        )
        self.db.add(db_alumni)
        self.db.commit()
        self.db.refresh(db_alumni)
        return db_alumni

    def update(self, alumni_id: int, alumni: schemas.AlumniUpdate):
        db_alumni = self.get_by_id(alumni_id)
        if not db_alumni:
            raise HTTPException(status_code=404, detail="Alumni not found")
        
        update_data = alumni.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_alumni, field, value)
        
        self.db.commit()
        self.db.refresh(db_alumni)
        return db_alumni

    def delete(self, alumni_id: int):
        db_alumni = self.get_by_id(alumni_id)
        if not db_alumni:
            raise HTTPException(status_code=404, detail="Alumni not found")
        
        self.db.delete(db_alumni)
        self.db.commit()
        return {"message": "Alumni deleted successfully"}