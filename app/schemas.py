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


class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(..., min_length=4)
    company: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NewsCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=250)
    content: str = Field(..., min_length=5)
    image_url: Optional[str] = None


class NewsUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=250)
    content: Optional[str] = Field(None, min_length=5)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class NewsResponse(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str] = None
    published_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    password: str
