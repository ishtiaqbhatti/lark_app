# core/serp_analyzers/featured_snippet_analyzer.py

from typing import Dict, Any


class FeaturedSnippetAnalyzer:
    def analyze(self, serp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes the featured snippet in the SERP."""
        analysis = {
            "serp_has_featured_snippet": "featured_snippet"
            in serp_data.get("item_types", []),
            "featured_snippet_content": None,
        }

        for item in serp_data.get("items", []):
            if item.get("type") == "featured_snippet":
                analysis["featured_snippet_content"] = item.get("description")
                break

        return analysis
