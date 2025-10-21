import logging
from typing import List, Dict, Any
from urllib.parse import urlparse

from backend.data_access.database_manager import DatabaseManager


class CannibalizationChecker:
    def __init__(
        self,
        target_domain: str,
        dataforseo_client: Any,
        client_cfg: Dict[str, Any],
        db_manager: DatabaseManager,
    ):
        self.target_domain = (
            target_domain.lower().replace("www.", "") if target_domain else None
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.dataforseo_client = dataforseo_client
        self.client_cfg = client_cfg
        self.db_manager = db_manager

    def is_url_in_serp(
        self, serp_results: List[Dict[str, Any]], keyword: str, client_id: str
    ) -> bool:
        """
        Returns True if the target domain is found in the list of SERP results
        OR if the keyword already exists in the opportunities database for the client.
        """
        if self.db_manager.check_existing_keywords(client_id, [keyword]):
            self.logger.warning(
                f"Cannibalization detected: Keyword '{keyword}' already exists in the database for client '{client_id}'."
            )
            return True

        if not self.target_domain:
            return False

        for result in serp_results:
            try:
                url = result.get("url")
                if not url:
                    continue
                url_domain = urlparse(url).netloc.lower().replace("www.", "")
                if url_domain == self.target_domain or url_domain.endswith(
                    f".{self.target_domain}"
                ):
                    self.logger.warning(
                        f"Cannibalization detected: Found '{url}' in SERP for '{keyword}'."
                    )
                    return True
            except Exception:
                continue
        return False
