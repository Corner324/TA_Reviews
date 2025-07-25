"""Sentiment analysis service with ML and dictionary approaches."""

from typing import Any

from app.ml.sentiment_model import SentimentMLModel


class SentimentService:
    """Service for analyzing sentiment of text using ML and dictionary approaches."""

    # Positive words dictionary (fallback method)
    POSITIVE_WORDS: set[str] = {
        "хорош", "люблю", "отлично", "супер", "замечательно",
        "прекрасно", "великолепно", "нравится", "классно",
        "отличный", "хороший", "превосходно", "восхитительно"
    }

    # Negative words dictionary (fallback method)
    NEGATIVE_WORDS: set[str] = {
        "плохо", "ненавиж", "ужасно", "отвратительно", "кошмар",
        "не нравится", "плохой", "худший", "провал", "ужас",
        "отвратительный", "кошмарный", "ненавижу"
    }

    def __init__(self, use_ml: bool = True):
        """
        Initialize sentiment service.

        Args:
            use_ml: Whether to use ML model (True) or dictionary approach (False)
        """
        self.use_ml = use_ml
        self.ml_model = None

        if self.use_ml:
            try:
                self.ml_model = SentimentMLModel()
                # Загружаем или обучаем модель при инициализации
                if not self.ml_model.is_model_trained():
                    print("Training ML model for the first time...")
                    self.ml_model.train()
                else:
                    self.ml_model.load_model()
            except Exception as e:
                print(f"Failed to initialize ML model: {e}")
                print("Falling back to dictionary approach")
                self.use_ml = False

    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of the given text.

        Args:
            text: Text to analyze

        Returns:
            Sentiment: 'positive', 'negative', or 'neutral'
        """
        if not text:
            return "neutral"

        # Try ML approach first
        if self.use_ml and self.ml_model:
            try:
                return self.ml_model.predict(text)
            except Exception as e:
                print(f"ML prediction failed: {e}, falling back to dictionary")
                # Fall back to dictionary approach
                pass

        # Dictionary approach (fallback)
        return self._analyze_with_dictionary(text)

    def analyze_sentiment_detailed(self, text: str) -> dict[str, Any]:
        """
        Analyze sentiment with detailed information including probabilities.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with sentiment, method used, and probabilities (if ML)
        """
        if not text:
            return {
                "sentiment": "neutral",
                "method": "empty_text",
                "probabilities": {"positive": 0.33, "negative": 0.33, "neutral": 0.34}
            }

        # Try ML approach first
        if self.use_ml and self.ml_model:
            try:
                sentiment = self.ml_model.predict(text)
                probabilities = self.ml_model.predict_proba(text)
                return {
                    "sentiment": sentiment,
                    "method": "machine_learning",
                    "probabilities": probabilities
                }
            except Exception as e:
                print(f"ML prediction failed: {e}")

        # Dictionary approach
        sentiment = self._analyze_with_dictionary(text)
        return {
            "sentiment": sentiment,
            "method": "dictionary",
            "probabilities": None
        }

    def _analyze_with_dictionary(self, text: str) -> str:
        """
        Analyze sentiment using dictionary approach.

        Args:
            text: Text to analyze

        Returns:
            Sentiment: 'positive', 'negative', or 'neutral'
        """
        # Normalize text to lowercase
        normalized_text = text.lower()

        # Count positive and negative words
        positive_count = sum(1 for word in self.POSITIVE_WORDS
                           if word in normalized_text)
        negative_count = sum(1 for word in self.NEGATIVE_WORDS
                           if word in normalized_text)

        # Determine predominant sentiment
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def retrain_model(self, additional_data: list = None):
        """
        Retrain the ML model with additional data.

        Args:
            additional_data: List of (text, label) tuples to add to training
        """
        if not self.use_ml:
            print("ML is disabled, cannot retrain model")
            return

        if not self.ml_model:
            self.ml_model = SentimentMLModel()

        try:
            if additional_data:
                from app.data.training_data import TRAINING_DATA
                combined_data = TRAINING_DATA + additional_data
                self.ml_model.train(combined_data)
            else:
                self.ml_model.train()
            print("Model retrained successfully")
        except Exception as e:
            print(f"Failed to retrain model: {e}")
