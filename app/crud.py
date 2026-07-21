from sqlalchemy.orm import Session

from app import models, schemas


def create_contact_message(db: Session, message: schemas.ContactMessageCreate) -> models.ContactMessage:
    db_message = models.ContactMessage(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def list_contact_messages(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.ContactMessage)
        .order_by(models.ContactMessage.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_news(db: Session, skip: int = 0, limit: int = 5):
    return (
        db.query(models.News)
        .filter(models.News.is_active == True)
        .order_by(models.News.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_news(db: Session) -> int:
    return db.query(models.News).filter(models.News.is_active == True).count()


def get_news_by_id(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id, models.News.is_active == True).first()
