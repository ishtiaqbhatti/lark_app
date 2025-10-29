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

    def group_by_category(self, opportunities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Groups a list of opportunities by their primary category.
        """
        opportunities_by_category = {}
        for opportunity in opportunities:
            # Safely access categories from the full_data JSON blob
            categories = opportunity.get("full_data", {}).get("keyword_info", {}).get("categories", [])
            
            # Use the first category for grouping, or "Uncategorized"
            primary_category = categories[0] if categories else "Uncategorized"
            
            if primary_category not in opportunities_by_category:
                opportunities_by_category[primary_category] = []
            opportunities_by_category[primary_category].append(opportunity)
        return opportunities_by_category

    def group_by_core_keyword(self, opportunities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Groups a list of opportunities by their core_keyword.
        """
        opportunities_by_core_keyword = {}
        for opportunity in opportunities:
            core_keyword = opportunity.get("full_data", {}).get("keyword_properties", {}).get("core_keyword")
            if not core_keyword:
                core_keyword = opportunity.get("keyword")

            if core_keyword not in opportunities_by_core_keyword:
                opportunities_by_core_keyword[core_keyword] = []
            opportunities_by_core_keyword[core_keyword].append(opportunity)
            
        return opportunities_by_core_keyword
