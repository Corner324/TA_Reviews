"""Reviews API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.models.schemas import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService
from app.api.dependencies import get_review_service

router = APIRouter()


@router.post("/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    review: ReviewCreate,
    service: ReviewService = Depends(get_review_service)
) -> ReviewResponse:
    """
    Create a new review with sentiment analysis.
    
    Args:
        review: Review data to create
        service: Review service dependency
        
    Returns:
        Created review with sentiment analysis
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        return service.create_review(review)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/reviews", response_model=List[ReviewResponse])
async def get_reviews(
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    service: ReviewService = Depends(get_review_service)
) -> List[ReviewResponse]:
    """
    Get all reviews with optional sentiment filtering.
    
    Args:
        sentiment: Optional sentiment filter (positive, negative, neutral)
        service: Review service dependency
        
    Returns:
        List of reviews matching the filter
        
    Raises:
        HTTPException: If filtering fails
    """
    try:
        return service.get_reviews(sentiment=sentiment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/reviews/analyze", response_model=dict)
async def analyze_sentiment_detailed(
    review: ReviewCreate,
    service: ReviewService = Depends(get_review_service)
) -> dict:
    """
    Analyze sentiment of text without saving to database.
    Returns detailed information including probabilities if ML is used.
    
    Args:
        review: Review data to analyze
        service: Review service dependency
        
    Returns:
        Detailed sentiment analysis result
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        return service.analyze_sentiment_detailed(review.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")