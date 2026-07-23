from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/contact", tags=["Contact"])


@router.post("", response_model=schemas.ContactMessageResponse, status_code=201)
def create_contact(
    payload: schemas.ContactMessageCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_contact_message(db, payload)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao salvar mensagem: {exc}",
        )


@router.get("", response_model=list[schemas.ContactMessageResponse])
def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_contact_messages(db, skip=skip, limit=limit)
