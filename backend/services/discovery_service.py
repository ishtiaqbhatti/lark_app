# services/discovery_service.py

from typing import Dict, Any
from data_access.database_manager import DatabaseManager


class DiscoveryService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_discovery_run(self, client_id: str, parameters: Dict[str, Any]) -> int:
        """Creates a new discovery run record and returns its ID."""
        return self.db_manager.create_discovery_run(client_id, parameters)

    def get_disqualification_reasons(self, run_id: int) -> Dict[str, int]:
        """
        Retrieves a summary of disqualification reasons for a specific discovery run.
        """
        keywords = self.db_manager.get_keywords_for_run(run_id)

        disqualification_reasons = {}
        for keyword in keywords:
            if keyword.get("blog_qualification_status") == "rejected":
                reason = keyword.get("blog_qualification_reason")
                if reason:
                    disqualification_reasons[reason] = (
                        disqualification_reasons.get(reason, 0) + 1
                    )

        return disqualification_reasons

    def get_all_discovery_runs_paginated(
        self, client_id: str, page: int, limit: int, filters: Dict[str, Any]
    ):
        """Retrieves all discovery runs for a specific client with pagination and filtering."""
        return self.db_manager.get_all_discovery_runs_paginated(
            client_id, page, limit, filters
        )

    def get_discovery_run_details(self, run_id: int) -> Dict[str, Any]:
        """
        Retrieves a single discovery run by its ID and enriches it with
        disqualification reasons.
        """
        run_details = self.db_manager.get_discovery_run_by_id(run_id)
        if run_details:
            disqualification_reasons = self.get_disqualification_reasons(run_id)
            run_details["disqualification_reasons_summary"] = disqualification_reasons
        return run_details

    def get_keywords_for_run(self, run_id: int):
        """Retrieves all keywords for a specific discovery run."""
        return self.db_manager.get_keywords_for_run(run_id)
