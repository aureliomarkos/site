# endereço IP: 163.176.237.220 da Oracle Cloud

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.seed import seed_news

from app.routes import clients, client_messages, contact, news, admin, chat


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

# ── CORS ─────────────────────────────────────────────────────────

origins = [origin.strip() for origin in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files ─────────────────────────────────────────────────

app.mount("/page", StaticFiles(directory="app/page", html=True), name="page")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/page/")


# ── Routers ──────────────────────────────────────────────────────

app.include_router(clients.router)
app.include_router(client_messages.router)
app.include_router(contact.router)
app.include_router(news.router)
app.include_router(admin.router)
app.include_router(chat.router)


