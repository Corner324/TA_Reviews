"""Business logic service for reviews."""

from datetime import datetime

from sqlalchemy.orm import Session

from app.config import settings
from app.models.schemas import ReviewCreate, ReviewResponse
from app.repositories.review_repository import ReviewRepository
from app.services.sentiment_service import SentimentService


class ReviewService:
    """Service for review business logic operations."""

    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.repository = ReviewRepository(db)
        self.sentiment_service = SentimentService(use_ml=settings.use_ml_sentiment)

    def create_review(self, review_data: ReviewCreate) -> ReviewResponse:
        """
        Create a new review with sentiment analysis.

        Args:
            review_data: Review creation data

        Returns:
            Created review response

        Raises:
            Exception: If creation fails
        """
        # Анализируем сентимент
        sentiment = self.sentiment_service.analyze_sentiment(review_data.text)

        # Подготавливаем данные отзыва
        review_dict = {
            "text": review_data.text,
            "sentiment": sentiment,
            "created_at": datetime.utcnow().isoformat(),
        }

        # Создаем отзыв в базе данных
        db_review = self.repository.create(review_dict)

        # Возвращаем ответ
        return ReviewResponse(
            id=db_review.id,
            text=db_review.text,
            sentiment=db_review.sentiment,
            created_at=db_review.created_at,
        )

    def get_reviews(self, sentiment: str = None) -> list[ReviewResponse]:
        """
        Get reviews with optional sentiment filtering.

        Args:
            sentiment: Optional sentiment filter

        Returns:
            List of review responses
        """
        # Проверяем параметр сентимента
        if sentiment and sentiment not in ["positive", "negative", "neutral"]:
            raise ValueError("Invalid sentiment value")

        # Получаем отзывы из репозитория
        db_reviews = self.repository.get_all(sentiment_filter=sentiment)

        # Преобразуем в объекты ответа
        return [
            ReviewResponse(
                id=review.id,
                text=review.text,
                sentiment=review.sentiment,
                created_at=review.created_at,
            )
            for review in db_reviews
        ]

    def analyze_sentiment_detailed(self, text: str) -> dict:
        """
        Analyze sentiment with detailed information.

        Args:
            text: Text to analyze

        Returns:
            Detailed sentiment analysis result
        """
        return self.sentiment_service.analyze_sentiment_detailed(text)
