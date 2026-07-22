import logging
from pathlib import Path

from sqlalchemy.orm import Session

from app import models, schemas

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "client_registration.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("client_registration")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(LOG_PATH)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)


def create_client(db: Session, client: schemas.ClientCreate) -> models.Client:
    existing = db.query(models.Client).filter(models.Client.email == client.email).first()
    if existing:
        logger.warning("Duplicate email registration attempted: %s", client.email)
        raise ValueError("email já existe")

    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    logger.info("Client registered successfully: %s", db_client.email)
    return db_client


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


def get_news_by_id_admin(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()


def create_news(db: Session, news: schemas.NewsCreate) -> models.News:
    db_news = models.News(title=news.title, content=news.content, image_url=news.image_url)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def update_news(db: Session, news_id: int, news: schemas.NewsUpdate) -> models.News | None:
    db_news = db.query(models.News).filter(models.News.id == news_id).first()
    if not db_news:
        return None
    update_data = news.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_news, key, value)
    db.commit()
    db.refresh(db_news)
    return db_news


def delete_news(db: Session, news_id: int) -> bool:
    db_news = db.query(models.News).filter(models.News.id == news_id).first()
    if not db_news:
        return False
    db.delete(db_news)
    db.commit()
    return True


def list_all_news_admin(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.News)
        .order_by(models.News.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
