from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/news", tags=["News"])


@router.get("", response_model=list[schemas.NewsResponse])
def list_news(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.list_news(db, skip=skip, limit=limit)


@router.get("/count")
def count_news(db: Session = Depends(get_db)):
    return {"total": crud.count_news(db)}


@router.get("/{news_id}", response_model=schemas.NewsResponse)
def get_news(news_id: int, db: Session = Depends(get_db)):
    news = crud.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return news
