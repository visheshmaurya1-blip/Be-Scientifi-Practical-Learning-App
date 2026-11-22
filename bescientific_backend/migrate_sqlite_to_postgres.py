"""Copy all data from a SQLite file into PostgreSQL (safe to re-run: existing rows are skipped).

    python migrate_sqlite_to_postgres.py sqlite:///./bescientific.db postgresql+psycopg2://u:p@host/db
"""
import sys
from sqlalchemy import create_engine, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database import Base
import app.models  # noqa: F401  (registers tables)

src_url, dst_url = sys.argv[1], sys.argv[2]
src, dst = create_engine(src_url), create_engine(dst_url)
Base.metadata.create_all(dst)

with src.connect() as s, dst.begin() as d:
    for table in Base.metadata.sorted_tables:       # parents before children
        rows = [dict(r) for r in s.execute(select(table)).mappings()]
        if rows:
            for i in range(0, len(rows), 1000):
                d.execute(pg_insert(table).on_conflict_do_nothing(), rows[i:i + 1000])
        print(f"{table.name}: {len(rows)} rows")
    # keep the sync cursor sequence ahead of copied rows
    d.execute(text("SELECT setval(pg_get_serial_sequence('sync_changes','seq'), "
                   "COALESCE((SELECT MAX(seq) FROM sync_changes), 1))"))
print("done")
