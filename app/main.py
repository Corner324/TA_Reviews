"""Main FastAPI application."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.reviews import router as reviews_router
from app.config import settings
from app.core.database import create_tables
from app.core.exceptions import ReviewServiceException

# Создаем FastAPI приложение
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Service for real-time sentiment analysis of user reviews",
    debug=settings.debug,
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(reviews_router, prefix=settings.api_v1_prefix, tags=["reviews"])


# Глобальные обработчики исключений
@app.exception_handler(ReviewServiceException)
async def review_service_exception_handler(
    request: Request, exc: ReviewServiceException
) -> JSONResponse:
    """Handle custom review service exceptions."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


# Событие запуска
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    create_tables()


# Эндпоинт проверки здоровья
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.project_name}
