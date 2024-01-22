from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class SchemaPostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    creator_email: str

class PostCreate(SchemaPostBase):
    pass

class PostResponse(BaseModel):
    title: str = Field(alias="Title of the Post")
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email_id: EmailStr
    password: str

class UserResponse(BaseModel):
    email_id: EmailStr
    created_at: datetime
