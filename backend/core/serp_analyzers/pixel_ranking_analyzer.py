# core/serp_analyzers/pixel_ranking_analyzer.py

from typing import Dict, Any


class PixelRankingAnalyzer:
    def analyze(self, serp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes the pixel ranking data in the SERP."""
        analysis = {
            "pixel_ranking_summary": None,
            "raw_pixel_ranking_data": [],
            "first_organic_y_pixel": None,
        }

        for item in serp_data.get("items", []):
            if item.get("rectangle"):
                analysis["raw_pixel_ranking_data"].append(
                    {
                        "type": item.get("type"),
                        "rank_group": item.get("rank_group"),
                        "rank_absolute": item.get("rank_absolute"),
                        "title": item.get("title"),
                        "rectangle": item.get("rectangle"),
                    }
                )

        if analysis["raw_pixel_ranking_data"]:
            top_organic_rects_y_coords = [
                r["rectangle"]["y"]
                for r in analysis["raw_pixel_ranking_data"]
                if r["type"] == "organic"
                and r.get("rank_absolute", 99) <= 3
                and "y" in r.get("rectangle", {})
            ]
            if top_organic_rects_y_coords:
                avg_y = sum(top_organic_rects_y_coords) / len(
                    top_organic_rects_y_coords
                )
                analysis["pixel_ranking_summary"] = (
                    f"Top 3 organic results start an average of {avg_y:.0f} pixels from the top of the page."
                )

        first_organic_result = next(
            (
                r
                for r in analysis["raw_pixel_ranking_data"]
                if r["type"] == "organic" and r.get("rank_absolute") == 1
            ),
            None,
        )
        if first_organic_result and "y" in first_organic_result.get("rectangle", {}):
            analysis["first_organic_y_pixel"] = first_organic_result["rectangle"]["y"]

        return analysis
