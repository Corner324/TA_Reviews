"""FastAPI dependencies."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.review_service import ReviewService


def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    """Dependency to get ReviewService instance."""
    return ReviewService(db)
