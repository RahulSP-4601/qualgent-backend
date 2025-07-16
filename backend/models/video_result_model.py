from sqlalchemy import Column, String, Text, DateTime
from backend.db.session import Base
from pydantic import BaseModel
from datetime import datetime

# SQLAlchemy ORM model (for DB table)
class VideoResultDB(Base):
    __tablename__ = "video_results"

    job_id = Column(String(255), primary_key=True, index=True)
    platform = Column(String(50))
    video_url = Column(Text)
    timestamp = Column(DateTime)

# Pydantic model (for API responses, internal use)
class VideoResult(BaseModel):
    job_id: str
    platform: str
    video_url: str
    timestamp: datetime

    class Config:
        orm_mode = True  # ✅ allows conversion from SQLAlchemy objects
