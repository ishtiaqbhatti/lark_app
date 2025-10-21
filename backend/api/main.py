# api/main.py
# api/main.py (New File, or existing FastAPI entry point)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # ADD THIS for Task 3
import logging
import os
import sys

# Add project root to sys.path to resolve imports from agents, pipeline, etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from your existing project structure
from app_config.manager import ConfigManager
from data_access.database_manager import DatabaseManager
from jobs import JobManager  # Import the class

from . import globals as api_globals


logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

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

    app.include_router(auth.router, prefix="/api")
    app.include_router(clients.router, prefix="/api")
    app.include_router(opportunities.router, prefix="/api")
    app.include_router(discovery.router, prefix="/api")
    app.include_router(orchestrator.router, prefix="/api")
    app.include_router(jobs.router, prefix="/api")
    app.include_router(qualification_settings.router, prefix="/api")
    app.include_router(qualification_strategies.router, prefix="/api")
    app.include_router(settings.router, prefix="/api")
