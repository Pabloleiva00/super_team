from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    first_name: str = None
    last_name: str = None
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    password: str = None

class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str = None
    last_name: str = None
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
