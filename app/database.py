from sqlmodel import SQLModel, create_engine, Session
import os
from sqlalchemy import event

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Detect database type
is_sqlite = DATABASE_URL.startswith("sqlite")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if is_sqlite else {}
)

# Only apply this for SQLite
if is_sqlite:
    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session