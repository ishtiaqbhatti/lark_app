# services/disqualification_service.py
import json
from typing import List, Dict, Any
from data_access.database_manager import DatabaseManager


class DisqualificationService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def disqualify(
        self, client_id: str, keywords: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Applies disqualification rules to a list of keywords.
        """
        qualification_settings = self.db_manager.get_qualification_settings(client_id)
        disqualification_rules = json.loads(
            qualification_settings.get("disqualification_rules", "[]")
        )

        brand_keywords = qualification_settings.get("brand_keywords", [])
        competitor_brand_keywords = qualification_settings.get(
            "competitor_brand_keywords", []
        )

        qualified_keywords = []
        for keyword in keywords:
            disqualified = False
            keyword_text = keyword.get("keyword", "").lower()

            if any(brand_kw in keyword_text for brand_kw in brand_keywords):
                continue

            if any(brand_kw in keyword_text for brand_kw in competitor_brand_keywords):
                continue

            for rule in disqualification_rules:
                field = rule.get("field")
                operator = rule.get("operator")
                value = rule.get("value")

                field_value = keyword
                for key in field.split("."):
                    field_value = field_value.get(key, {})

                if operator == "=" and field_value == value:
                    disqualified = True
                    break
                elif operator == ">" and field_value > value:
                    disqualified = True
                    break
                elif operator == "<" and field_value < value:
                    disqualified = True
                    break

            if not disqualified:
                qualified_keywords.append(keyword)

        return qualified_keywords
