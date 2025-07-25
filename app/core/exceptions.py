"""Custom exceptions for the application."""


class ReviewServiceException(Exception):
    """Base exception for review service operations."""
    pass


class EmptyTextException(ReviewServiceException):
    """Exception raised when review text is empty."""
    pass


class DatabaseException(ReviewServiceException):
    """Exception raised for database operation errors."""
    pass
