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
