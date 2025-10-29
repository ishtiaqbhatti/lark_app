from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # ... existing settings ...
    
    # CORS - Be explicit about allowed origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # In production, load from environment variable
    if os.getenv("ENVIRONMENT") == "production":
        CORS_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
    
    # Other CORS settings
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_MAX_AGE: int = 600  # 10 minutes
    
    class Config:
        case_sensitive = True

settings = Settings()
