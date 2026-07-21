# MarkosDev Backend

Backend FastAPI + SQLAlchemy para o portfólio MarkosDev.

## Funcionalidades

- Recebe mensagens do formulário de contato via `POST /api/contact`
- Persiste em banco SQLite (padrão) — pode ser trocado por PostgreSQL/MySQL via `DATABASE_URL`
- Lista mensagens via `GET /api/contact`

## Estrutura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py       # aplicação FastAPI e endpoints
│   ├── config.py     # configurações via .env
│   ├── database.py   # engine, sessão e base declarativa
│   ├── models.py     # modelos SQLAlchemy
│   ├── schemas.py    # schemas Pydantic
│   └── crud.py       # operações no banco
├── requirements.txt
└── .env.example
```

## Instalação

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
```

## Execução

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse a documentação interativa em: http://localhost:8000/docs

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário:

```env
DATABASE_URL=sqlite:///./markosdev.db
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Health check |
| POST | `/api/contact` | Criar mensagem de contato |
| GET | `/api/contact` | Listar mensagens de contato |
