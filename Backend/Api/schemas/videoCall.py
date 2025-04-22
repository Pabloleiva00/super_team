from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VideoCallCreate(BaseModel):
    caller_id: Optional[int] = None
    receiver_id: Optional[int] = None
    started_at: datetime
    ended_at: datetime = None
    duration: int = None
    status: str = "pending"

class VideoCallUpdate(BaseModel):
    caller_id: Optional[int] = None
    receiver_id: Optional[int] = None
    started_at: datetime = None
    ended_at: datetime = None
    duration: int = None
    status: str = None
