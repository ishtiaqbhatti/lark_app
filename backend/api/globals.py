# api/globals.py
from typing import Optional
from app_config.manager import ConfigManager
from data_access.database_manager import DatabaseManager
from jobs import JobManager

config_manager: Optional[ConfigManager] = None
db_manager: Optional[DatabaseManager] = None
job_manager: Optional[JobManager] = None
