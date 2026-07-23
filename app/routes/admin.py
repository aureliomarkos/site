from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def verify_admin(password: str = Header(alias="x-admin-password")):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=401,
            detail="Senha administrativa inválida",
        )
    return True


# ── Login ────────────────────────────────────────────────────────

@router.post("/login")
def admin_login(payload: schemas.AdminLogin):
    if payload.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Senha inválida")
    return {"success": True, "message": "Autenticado com sucesso"}


# ── Notícias ─────────────────────────────────────────────────────

@router.get("/news", response_model=list[schemas.NewsResponse])
def admin_list_news(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    return crud.list_all_news_admin(db, skip=skip, limit=limit)


@router.get("/news/{news_id}", response_model=schemas.NewsResponse)
def admin_get_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    news = crud.get_news_by_id_admin(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return news


@router.post("/news", response_model=schemas.NewsResponse, status_code=201)
def admin_create_news(
    payload: schemas.NewsCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    return crud.create_news(db, payload)


@router.put("/news/{news_id}", response_model=schemas.NewsResponse)
def admin_update_news(
    news_id: int,
    payload: schemas.NewsUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    news = crud.update_news(db, news_id, payload)
    if not news:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return news


@router.delete("/news/{news_id}")
def admin_delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    deleted = crud.delete_news(db, news_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return {"success": True, "message": "Notícia excluída com sucesso"}


# ── Mensagens dos Clientes ───────────────────────────────────────

@router.get("/client-messages", response_model=list[schemas.AdminClientMessageResponse])
def admin_list_client_messages(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    return crud.list_all_client_messages_admin(db)


@router.put("/client-messages/{message_id}", response_model=schemas.AdminClientMessageResponse)
def admin_update_client_message(
    message_id: int,
    payload: schemas.ClientMessageUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    updated = crud.admin_update_client_message(db, message_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return updated
