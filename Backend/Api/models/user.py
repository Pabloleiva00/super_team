from sqlalchemy import Column, DateTime, func
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships with VideoCall
    calls_made = relationship("VideoCall", foreign_keys="[VideoCall.caller_id]", back_populates="caller")
    calls_received = relationship("VideoCall", foreign_keys="[VideoCall.receiver_id]", back_populates="receiver")