import json
from datetime import datetime
import os
import sys

# Add project root to sys.path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app_config.manager import ConfigManager
from backend.data_access.database_manager import DatabaseManager

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def export_database_to_json():
    """
    Connects to the database, fetches all opportunities, and exports them to a JSON file.
    """
    print("Starting database export...")
    try:
        settings_file_path = os.path.join(os.path.dirname(__file__), "app_config", "settings.ini")
        config_manager = ConfigManager(settings_path=settings_file_path)
        db_manager = DatabaseManager(cfg_manager=config_manager)
        
        print("Fetching all opportunities from the database...")
        all_opportunities = db_manager.get_all_opportunities_for_export()
        print(f"Found {len(all_opportunities)} opportunities to export.")
        
        # Define the output file path in the project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        output_file_path = os.path.join(project_root, "database_export.json")
        
        print(f"Exporting data to {output_file_path}...")
        with open(output_file_path, "w") as f:
            json.dump(all_opportunities, f, indent=4, default=json_serial)
            
        print("Database export completed successfully.")
        
    except Exception as e:
        print(f"An error occurred during the export process: {e}")

if __name__ == "__main__":
    export_database_to_json()
