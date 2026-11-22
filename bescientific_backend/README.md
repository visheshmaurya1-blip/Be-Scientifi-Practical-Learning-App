# Be Scientific Backend (FastAPI)

    pip install -r requirements.txt
    cp .env.example .env   # set ADMIN_KEY, DATABASE_URL
    export ADMIN_KEY=your-secret
    uvicorn app.main:app --reload      # docs at http://localhost:8000/docs
    pytest -q tests

Switch DB: `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/bescientific`
Move SQLite data to Postgres: `python migrate_sqlite_to_postgres.py sqlite:///./bescientific.db <postgres-url>`

Flow: admin creates school (gets api_key) -> school adds students -> tablets use client_sync.py offline ->
POST /sync/push + GET /sync/pull -> /analytics/* endpoints.
