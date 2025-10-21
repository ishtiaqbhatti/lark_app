import logging
import os
import sys

# Ensure the project root is in sys.path for module imports
# Correctly identify the project root, which is two levels above the 'backend' directory
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
backend_root = os.path.join(project_root, "backend")

# Add the backend directory to sys.path to allow for absolute imports from the backend module
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

# Import necessary classes from your project
try:
    from app_config.manager import ConfigManager
    from data_access.database_manager import DatabaseManager
except ImportError as e:
    print(f"Error importing project modules: {e}")
    print(
        "Please ensure you are running this script from the project's root directory or that paths are set up correctly."
    )
    print(f"Current working directory: {os.getcwd()}")
    print(f"Project root: {project_root}")
    print(f"Backend root added to sys.path: {backend_root}")
    sys.exit(1)

# Configure logging for this script run
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def main():
    """Initializes the database, runs migrations, and seeds the default client."""

    logger.info(
        "Starting database initialization and default client seeding process..."
    )

    # Construct the absolute path to the settings.ini file
    settings_path = os.path.join(backend_root, "app_config", "settings.ini")
    if not os.path.exists(settings_path):
        logger.error(f"settings.ini file not found at expected path: {settings_path}")
        sys.exit(1)

    # Instantiate ConfigManager with the correct path
    config_manager = ConfigManager(settings_path=settings_path)
    global_cfg = config_manager.get_global_config()
    db_file_name = global_cfg.get(
        "db_file_name", "data/opportunities.db"
    )  # Get DB file name from config

    # The database path is relative to the project root
    db_path = os.path.join(project_root, db_file_name)
    db_data_dir = os.path.dirname(db_path)

    # --- Force re-creation of the database ---
    if os.path.exists(db_path):
        logger.info(
            f"Deleting existing database file at {db_path} to ensure a clean slate."
        )
        os.remove(db_path)
    # Ensure the data directory exists
    if not os.path.exists(db_data_dir):
        os.makedirs(db_data_dir)
        logger.info(f"Created data directory: {db_data_dir}")
    # --- End ---

    try:
        # 1. Initialize DatabaseManager
        db_manager = DatabaseManager(cfg_manager=config_manager, db_path=db_path)

        # 2. Ensure database and all tables are created, and migrations are applied
        db_manager.initialize()
        logger.info("Database initialized and all migrations applied.")

        # 3. Define default client details (using values from settings.ini)
        client_id = global_cfg.get("default_client_id", "Lark_Main_Site")
        client_name = client_id.replace(
            "_", " "
        ).title()  # Simple conversion for display name

        # 4. Get default settings template (which includes brand voice settings from settings.ini)
        default_settings = config_manager.get_default_client_settings_template()

        if not default_settings:
            logger.error("Could not load default client settings template. Aborting.")
            return

        # 5. Add the default client
        success = db_manager.add_client(client_id, client_name, default_settings)

        if success:
            logger.info(
                f"Successfully seeded the database with default client: '{client_name}' ({client_id})"
            )
        else:
            # This would only happen if the client_id already existed, which shouldn't after deleting the DB.
            logger.warning(
                f"Default client '{client_name}' ({client_id}) already existed in the database."
            )

        logger.info("Database setup process complete. No keyword data has been added.")

    except Exception as e:
        logger.error(f"An error occurred during database setup: {e}", exc_info=True)


if __name__ == "__main__":
    main()
