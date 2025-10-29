"""
Custom exceptions for consistent error handling.
"""

from fastapi import HTTPException
from typing import Optional, Dict, Any

class BaseAPIException(HTTPException):
    """Base exception for API errors."""
    
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        error_code: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.extra = extra or {}

class ValidationException(BaseAPIException):
    """Raised when input validation fails."""
    
    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            status_code=400,
            detail=detail,
            error_code="VALIDATION_ERROR",
            extra={"field": field} if field else {}
        )

class ResourceNotFoundException(BaseAPIException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: Any):
        super().__init__(
            status_code=404,
            detail=f"{resource_type} with ID {resource_id} not found.",
            error_code="RESOURCE_NOT_FOUND",
            extra={"resource_type": resource_type, "resource_id": str(resource_id)}
        )

class DataForSEOAPIException(BaseAPIException):
    """Raised when DataForSEO API call fails."""
    
    def __init__(self, detail: str, status_code: int = 502):
        super().__init__(
            status_code=status_code,
            detail=f"DataForSEO API error: {detail}",
            error_code="EXTERNAL_API_ERROR"
        )

class RateLimitException(BaseAPIException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=429,
            detail=f"Rate limit exceeded. Please try again in {retry_after} seconds.",
            error_code="RATE_LIMIT_EXCEEDED",
            extra={"retry_after": retry_after}
        )
