# api/main.py
# api/main.py (New File, or existing FastAPI entry point)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # ADD THIS for Task 3
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import os
import sys

# Add project root to sys.path to resolve imports from agents, pipeline, etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.middleware.cors import CORSMiddleware
from app_config.config import settings
# Import from your existing project structure
from app_config.manager import ConfigManager
from data_access.database_manager import DatabaseManager
from jobs import JobManager  # Import the class

from .routers import (
    auth,
    clients,
    opportunities,
    discovery,
    orchestrator,
    jobs,
    qualification_settings,
    qualification_strategies,
    settings,
)
from . import globals as api_globals


logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# STRICTER CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Explicit list only
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    max_age=settings.CORS_MAX_AGE,
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Mount the static directory for generated images
# Images will be accessible at /api/images/{filename}
static_images_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "generated_images")
)
app.mount(
    "/api/images", StaticFiles(directory=static_images_path), name="static_images"
)


# --- Global Dependency Initialization (simplified for example) ---
# In a real app, use @lru_cache or proper dependency injection
@app.on_event("startup")
async def startup_event():
    api_globals.config_manager = ConfigManager()
    api_globals.db_manager = DatabaseManager(cfg_manager=api_globals.config_manager)
    api_globals.db_manager.initialize()  # Ensure DB tables are created/migrated
    api_globals.job_manager = JobManager(
        db_manager=api_globals.db_manager
    )  # Initialize JobManager with db_manager

    logger.info("FastAPI application startup complete. Dependencies initialized.")

    app.include_router(auth.router)
    app.include_router(clients.router)
    app.include_router(opportunities.router)
    app.include_router(discovery.router)
    app.include_router(orchestrator.router)
    app.include_router(jobs.router)
    app.include_router(qualification_settings.router)
    app.include_router(qualification_strategies.router)
    app.include_router(settings.router)
    app.include_router(auth.router, prefix="/api")
    app.include_router(clients.router, prefix="/api")
    app.include_router(opportunities.router, prefix="/api")
    app.include_router(discovery.router, prefix="/api")
    app.include_router(orchestrator.router, prefix="/api")
    app.include_router(jobs.router, prefix="/api")
    app.include_router(qualification_settings.router, prefix="/api")
    app.include_router(qualification_strategies.router, prefix="/api")
    app.include_router(settings.router, prefix="/api")
