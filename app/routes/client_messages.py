from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/clients/{client_id}/messages", tags=["Client Messages"])


@router.post("", response_model=schemas.ClientMessageResponse, status_code=201)
def create_client_message(
    client_id: int,
    payload: schemas.ClientMessageCreate,
    db: Session = Depends(get_db),
):
    return crud.create_client_message(db, client_id, payload)


@router.get("", response_model=list[schemas.ClientMessageResponse])
def list_client_messages(client_id: int, db: Session = Depends(get_db)):
    return crud.list_client_messages(db, client_id)


@router.put("/{message_id}", response_model=schemas.ClientMessageResponse)
def update_client_message(
    client_id: int,
    message_id: int,
    payload: schemas.ClientMessageUpdate,
    db: Session = Depends(get_db),
):
    updated = crud.update_client_message(db, client_id, message_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="mensagem não encontrada")
    return updated


@router.delete("/{message_id}")
def delete_client_message(client_id: int, message_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_client_message(db, client_id, message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="mensagem não encontrada")
    return {"success": True, "message": "Mensagem removida com sucesso"}
