import logging
from datetime import datetime
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


def authenticate_client(db: Session, payload: schemas.ClientLogin):
    client = db.query(models.Client).filter(models.Client.email == payload.email).first()
    if not client or client.password != payload.password:
        raise ValueError("credenciais inválidas")
    return client


def create_client_message(db: Session, client_id: int, message: schemas.ClientMessageCreate) -> models.ClientMessage:
    db_message = models.ClientMessage(client_id=client_id, **message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def list_client_messages(db: Session, client_id: int):
    return (
        db.query(models.ClientMessage)
        .filter(models.ClientMessage.client_id == client_id)
        .order_by(models.ClientMessage.created_at.desc())
        .all()
    )


def list_all_client_messages_admin(db: Session):
    rows = (
        db.query(models.ClientMessage, models.Client.name, models.Client.email)
        .join(models.Client, models.ClientMessage.client_id == models.Client.id)
        .order_by(models.ClientMessage.created_at.desc())
        .all()
    )
    results = []
    for msg, client_name, client_email in rows:
        results.append({
            "id": msg.id,
            "client_id": msg.client_id,
            "client_name": client_name,
            "client_email": client_email,
            "title": msg.title,
            "message": msg.message,
            "attachment": msg.attachment,
            "status": msg.status,
            "message_response": msg.message_response,
            "created_at": msg.created_at,
            "updated_at": msg.updated_at,
        })
    return results


def admin_update_client_message(db: Session, message_id: int, message: schemas.ClientMessageUpdate):
    db_message = (
        db.query(models.ClientMessage)
        .filter(models.ClientMessage.id == message_id)
        .first()
    )
    if not db_message:
        return None

    update_data = message.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_message, key, value)
    db_message.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_message)

    client = db.query(models.Client).filter(models.Client.id == db_message.client_id).first()
    return {
        "id": db_message.id,
        "client_id": db_message.client_id,
        "client_name": client.name if client else "",
        "client_email": client.email if client else "",
        "title": db_message.title,
        "message": db_message.message,
        "attachment": db_message.attachment,
        "status": db_message.status,
        "message_response": db_message.message_response,
        "created_at": db_message.created_at,
        "updated_at": db_message.updated_at,
    }


def update_client_message(db: Session, client_id: int, message_id: int, message: schemas.ClientMessageUpdate):
    db_message = (
        db.query(models.ClientMessage)
        .filter(models.ClientMessage.id == message_id, models.ClientMessage.client_id == client_id)
        .first()
    )
    if not db_message:
        return None

    update_data = message.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_message, key, value)
    db_message.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_client_message(db: Session, client_id: int, message_id: int) -> bool:
    db_message = (
        db.query(models.ClientMessage)
        .filter(models.ClientMessage.id == message_id, models.ClientMessage.client_id == client_id)
        .first()
    )
    if not db_message:
        return False
    db.delete(db_message)
    db.commit()
    return True


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
