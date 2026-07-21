from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from app.database import Base


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    published_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
