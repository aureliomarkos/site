from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    subject: str = Field(..., min_length=2, max_length=200)
    message: str = Field(..., min_length=5)


class ContactMessageResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class NewsResponse(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str] = None
    published_at: datetime

    class Config:
        from_attributes = True
