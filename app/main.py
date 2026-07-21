# endereço IP: 163.176.237.220 da Oracle Cloud
# DeepSeek-V4-Flash-Max

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db
from app import schemas, crud
from app.seed import seed_news


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_news()
    yield


app = FastAPI(
    title="MarkosDev API",
    description="Backend do portfólio MarkosDev — formulário de contato e blog.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [origin.strip() for origin in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve arquivos
app.mount("/page", StaticFiles(directory="app/page", html=True), name="page")


# Se alguém acessar /
@app.get("/", include_in_schema=False)
def admin_index():
    return RedirectResponse("/page/")


@app.post("/api/contact", response_model=schemas.ContactMessageResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: schemas.ContactMessageCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_contact_message(db, payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar mensagem: {exc}",
        )


@app.get("/api/contact", response_model=list[schemas.ContactMessageResponse])
def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_contact_messages(db, skip=skip, limit=limit)


@app.get("/api/news", response_model=list[schemas.NewsResponse])
def list_news(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.list_news(db, skip=skip, limit=limit)


@app.get("/api/news/count")
def count_news(db: Session = Depends(get_db)):
    return {"total": crud.count_news(db)}


@app.get("/api/news/{news_id}", response_model=schemas.NewsResponse)
def get_news(news_id: int, db: Session = Depends(get_db)):
    news = crud.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notícia não encontrada")
    return news


# ============================================
# Painel Administrativo — CRUD de notícias
# ============================================

from fastapi import Header
from app.config import settings


def verify_admin(password: str = Header(alias="x-admin-password")):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha administrativa inválida",
        )
    return True


@app.post("/api/admin/login")
def admin_login(payload: schemas.AdminLogin):
    if payload.password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha inválida",
        )
    return {"success": True, "message": "Autenticado com sucesso"}


@app.get("/api/admin/news", response_model=list[schemas.NewsResponse])
def admin_list_news(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    return crud.list_all_news_admin(db, skip=skip, limit=limit)


@app.get("/api/admin/news/{news_id}", response_model=schemas.NewsResponse)
def admin_get_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    news = crud.get_news_by_id_admin(db, news_id)
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notícia não encontrada")
    return news


@app.post(
    "/api/admin/news",
    response_model=schemas.NewsResponse,
    status_code=status.HTTP_201_CREATED,
)
def admin_create_news(
    payload: schemas.NewsCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    return crud.create_news(db, payload)


@app.put("/api/admin/news/{news_id}", response_model=schemas.NewsResponse)
def admin_update_news(
    news_id: int,
    payload: schemas.NewsUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    news = crud.update_news(db, news_id, payload)
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notícia não encontrada")
    return news


@app.delete("/api/admin/news/{news_id}")
def admin_delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin),
):
    deleted = crud.delete_news(db, news_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notícia não encontrada")
    return {"success": True, "message": "Notícia excluída com sucesso"}


