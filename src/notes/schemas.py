from pydantic import BaseModel
from datetime import datetime

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True