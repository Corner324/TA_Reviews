"""Simple ML model for sentiment analysis."""

import os

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from app.data.training_data import TRAINING_DATA


class SentimentMLModel:
    """Simple ML model for sentiment analysis using Naive Bayes."""

    def __init__(self):
        """Initialize the ML model."""
        self.model = None
        self.model_path = "app/ml/sentiment_model.joblib"
        self._create_pipeline()

    def _create_pipeline(self):
        """Create ML pipeline with TF-IDF and Naive Bayes."""
        self.model = Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        lowercase=True,
                        max_features=1000,
                        ngram_range=(1, 2),  # Учитываем биграммы
                        stop_words=None,  # Для русского языка оставляем все слова
                    ),
                ),
                ("classifier", MultinomialNB(alpha=1.0)),
            ]
        )

    def train(self, training_data: list[tuple[str, str]] = None):
        """
        Train the model on provided data.

        Args:
            training_data: List of (text, label) tuples
        """
        if training_data is None:
            training_data = TRAINING_DATA

        # Разделяем тексты и метки
        texts = [item[0] for item in training_data]
        labels = [item[1] for item in training_data]

        # Разделяем на train/test для оценки качества
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )

        # Обучаем модель
        self.model.fit(X_train, y_train)

        # Оцениваем качество
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.3f}")

        # Сохраняем модель
        self.save_model()

    def predict(self, text: str) -> str:
        """
        Predict sentiment for given text.

        Args:
            text: Text to analyze

        Returns:
            Predicted sentiment: 'positive', 'negative', or 'neutral'
        """
        if not self.model:
            self.load_model()

        if not text or not text.strip():
            return "neutral"

        try:
            prediction = self.model.predict([text.strip()])[0]
            return prediction
        except Exception:
            # Возврат "neutral" при ошибке предсказания
            return "neutral"

    def predict_proba(self, text: str) -> dict:
        """
        Get prediction probabilities for all classes.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with probabilities for each sentiment
        """
        if not self.model:
            self.load_model()

        if not text or not text.strip():
            return {"positive": 0.33, "negative": 0.33, "neutral": 0.34}

        try:
            probabilities = self.model.predict_proba([text.strip()])[0]
            classes = self.model.classes_
            return dict(zip(classes, probabilities, strict=False))
        except Exception:
            return {"positive": 0.33, "negative": 0.33, "neutral": 0.34}

    def save_model(self):
        """Save trained model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        """Load trained model from disk."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            print("No saved model found, training new model...")
            self.train()

    def is_model_trained(self) -> bool:
        """Check if model is trained and ready."""
        return os.path.exists(self.model_path) or self.model is not None
