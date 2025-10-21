# services/opportunities_service.py

from typing import List, Dict, Any, Tuple
from data_access.database_manager import DatabaseManager


class OpportunitiesService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_all_opportunities(
        self, client_id: str, params: Dict[str, Any]
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Retrieves keyword opportunities for a client, supporting filtering, sorting, and pagination.
        Returns (opportunities_list, total_count).
        """
        return self.db_manager.get_all_opportunities(client_id, params)

    def get_all_opportunities_summary(
        self, client_id: str, params: Dict[str, Any], select_columns: str = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Retrieves a lightweight summary of keyword opportunities for a client.
        Returns (opportunities_list, total_count).
        """
        return self.db_manager.get_all_opportunities(
            client_id, params, summary=True, select_columns=select_columns
        )

    def get_opportunities_by_category(
        self, client_id: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieves all opportunities for a client, grouped by category.
        """
        opportunities, _ = self.db_manager.get_all_opportunities(client_id, {})

        opportunities_by_category = {}
        for opportunity in opportunities:
            categories = opportunity.get("keyword_info", {}).get("categories", [])
            for category in categories:
                if category not in opportunities_by_category:
                    opportunities_by_category[category] = []
                opportunities_by_category[category].append(opportunity)

        return opportunities_by_category

    def get_opportunities_by_cluster(
        self, client_id: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieves all opportunities for a client, grouped by cluster.
        """
        opportunities, _ = self.db_manager.get_all_opportunities(client_id, {})

        opportunities_by_cluster = {}
        for opportunity in opportunities:
            cluster_name = opportunity.get("cluster_name")
            if cluster_name:
                if cluster_name not in opportunities_by_cluster:
                    opportunities_by_cluster[cluster_name] = []
                opportunities_by_cluster[cluster_name].append(opportunity)

        return opportunities_by_cluster
