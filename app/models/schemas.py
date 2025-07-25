"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, validator


class ReviewCreate(BaseModel):
    """Schema for creating a new review."""

    text: str

    @validator('text')
    def text_must_not_be_empty(cls, v):
        """Validate that text is not empty."""
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()


class ReviewResponse(BaseModel):
    """Schema for review response."""

    id: int
    text: str
    sentiment: str
    created_at: str

    class Config:
        from_attributes = True
