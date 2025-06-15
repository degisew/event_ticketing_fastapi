from typing import Annotated, Any, Generator
from contextlib import contextmanager
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings

DB_USER = settings.DB_USER
DB_PASS = settings.DB_PASS
DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME

url: str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine: Engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


# A cutom manager for atomic transaction
@contextmanager
def atomic_transaction(db: DbSession):
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise
