"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.database import Base

# Создаем SQLAlchemy движок
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # Необходимо для SQLite
)

# Создаем класс SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
