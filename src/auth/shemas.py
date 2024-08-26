from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic import BaseModel

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime