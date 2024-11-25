from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Alumni(Base):
    __tablename__ = "alumni"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    graduation_year = Column(Integer)
    degree = Column(String)
    major = Column(String)
    current_job = Column(String, nullable=True)
    company = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)

    # Matching relationship name
    user = relationship("User", back_populates="alumni")