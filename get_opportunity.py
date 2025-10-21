import json
from backend.data_access.database_manager import DatabaseManager
from backend.app_config.manager import ConfigManager


def get_opportunity_data(opportunity_id: int):
    """Connects to the database and fetches a single opportunity, including job status."""
    config_manager = ConfigManager()
    db_manager = DatabaseManager(cfg_manager=config_manager)

    opportunity = db_manager.get_opportunity_by_id(opportunity_id)

    if opportunity:
        # The data is already a dict-like object, so we can just print it.
        # The `full_data` field is a JSON string, so we should parse it.
        if opportunity.get("full_data") and isinstance(opportunity["full_data"], str):
            try:
                opportunity["full_data"] = json.loads(opportunity["full_data"])
            except json.JSONDecodeError:
                opportunity["full_data"] = "Error: Could not decode JSON."

        # Fetch job information if a job ID exists
        job_id = opportunity.get("latest_job_id")
        if job_id:
            job_info = db_manager.get_job(job_id)
            if job_info:
                opportunity["job_status"] = {
                    "id": job_info.get("id"),
                    "status": job_info.get("status"),
                    "progress": job_info.get("progress"),
                    "error": job_info.get("error"),
                    "started_at": job_info.get("started_at"),
                    "finished_at": job_info.get("finished_at"),
                }

        # Check for ai_content before writing
        if opportunity.get("ai_content"):
            print("ai_content is present in the fetched data.")
        else:
            print("ai_content is MISSING from the fetched data.")

        output_filename = f"opportunity_{opportunity_id}.json"
        with open(output_filename, "w") as f:
            json.dump(opportunity, f, indent=4)
        print(f"Opportunity data saved to {output_filename}")
    else:
        error_message = {"error": f"Opportunity with ID {opportunity_id} not found."}
        output_filename = f"opportunity_{opportunity_id}_error.json"
        with open(output_filename, "w") as f:
            json.dump(error_message, f, indent=4)
        print(f"Error message saved to {output_filename}")


if __name__ == "__main__":
    get_opportunity_data(3)