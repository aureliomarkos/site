from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.post("", response_model=schemas.ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: schemas.ClientCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_client(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except Exception as exc:
        crud.logger.exception("Unexpected client registration error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="servidor fora do ar",
        ) from exc


@router.post("/login", response_model=schemas.ClientResponse)
def login_client(payload: schemas.ClientLogin, db: Session = Depends(get_db)):
    try:
        client = crud.authenticate_client(db, payload)
        return client
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
