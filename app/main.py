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


@app.get("/")
def read_root():
    return {"message": "MarkosDev API online", "docs": "/docs"}


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


