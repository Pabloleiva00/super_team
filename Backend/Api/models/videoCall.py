from sqlalchemy import Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.sql.sqltypes import Integer, Enum
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Enum as SQLAlchemyEnum

import datetime


class VideoCall(Base):
    __tablename__ = "video_calls"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration = Column(Integer)  # Duration in seconds
    status = Column(SQLAlchemyEnum("pending", "in_progress", "finished", "failed", "refused", name="video_call_status"), default="pending")    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Foreign Keys to User
    caller_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))

    # Relationships to User
    caller = relationship("User", foreign_keys=[caller_id], back_populates="calls_made")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="calls_received")
