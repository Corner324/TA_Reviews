"""SQLAlchemy database models."""

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Review(Base):
    """Review model for storing user reviews with sentiment analysis."""
    
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    created_at = Column(String(50), nullable=False)
    
    def __repr__(self):
        return f"<Review(id={self.id}, sentiment='{self.sentiment}')>"