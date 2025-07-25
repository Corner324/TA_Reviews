"""Repository for review data access operations."""

from sqlalchemy.orm import Session

from app.models.database import Review


class ReviewRepository:
    """Repository for managing review data operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(self, review_data: dict) -> Review:
        """
        Create a new review in the database.

        Args:
            review_data: Dictionary containing review data

        Returns:
            Created Review object

        Raises:
            Exception: If database operation fails
        """
        try:
            db_review = Review(**review_data)
            self.db.add(db_review)
            self.db.commit()
            self.db.refresh(db_review)
            return db_review
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create review: {str(e)}")

    def get_all(self, sentiment_filter: str | None = None) -> list[Review]:
        """
        Get all reviews with optional sentiment filtering.

        Args:
            sentiment_filter: Optional sentiment to filter by

        Returns:
            List of Review objects

        Raises:
            Exception: If database operation fails
        """
        try:
            query = self.db.query(Review)

            if sentiment_filter:
                query = query.filter(Review.sentiment == sentiment_filter)

            return query.all()
        except Exception as e:
            raise Exception(f"Failed to get reviews: {str(e)}")
